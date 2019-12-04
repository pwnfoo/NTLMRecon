from urllib.parse import urlparse
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import urllib3
import sys
import base64
import struct
import string
import collections
from random import choice
import json



# We are hackers. SSL warnings don't stop us, although this is not recommended.
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# Decoder taken from https://gist.github.com/aseering/829a2270b72345a1dc42 , ported and modified
VALID_CHRS = set(string.ascii_letters + string.digits + string.punctuation)

FOUND_DOMAINS = ['google.com']

def clean_str(st):
    return ''.join((s if s in VALID_CHRS else '?') for s in st)


class StrStruct(object):
    def __init__(self, pos_tup, raw):
        length, alloc, offset = pos_tup
        self.length = length
        self.alloc = alloc
        self.offset = offset
        self.raw = raw[offset:offset + length]
        self.utf16 = False

        if len(self.raw) >= 2 and self.raw[1] == '\0':
            self.string = self.raw.decode('utf-16')
            self.utf16 = True
        else:
            self.string = self.raw

    def __str__(self):
        st = "%s'%s' [%s] (%db @%d)" % ('u' if self.utf16 else '',
                                        clean_str(self.string),
                                        self.raw,
                                        self.length, self.offset)
        if self.alloc != self.length:
            st += " alloc: %d" % self.alloc
        return st


msg_types = collections.defaultdict(lambda: "UNKNOWN")
msg_types[1] = "Request"
msg_types[2] = "Challenge"
msg_types[3] = "Response"

target_field_types = collections.defaultdict(lambda: "UNKNOWN")
target_field_types[0] = "TERMINATOR"
target_field_types[1] = "Server name"
target_field_types[2] = "AD domain name"
target_field_types[3] = "FQDN"
target_field_types[4] = "DNS domain name"
target_field_types[5] = "Parent DNS domain"


def decode_ntlm_str(st_raw):
    try:
        st = base64.b64decode(st_raw)
    except Exception as e:
        print("Input is not a valid base64-encoded string")
        return
    if st[:7] == b"NTLMSSP":
        pass
    else:
        print("Decode failed. NTLMSSP header not found at start of input string")
        return False

    return get_server_details(st)


def opt_str_struct(name, st, offset):
    nxt = st[offset:offset + 8]
    if len(nxt) == 8:
        hdr_tup = struct.unpack("<hhi", nxt)
        print("%s: %s" % (name, StrStruct(hdr_tup, st)))
    else:
        print("%s: [omitted]" % name)


def get_server_details(st):
    nxt = st[40:48]
    if len(nxt) == 8:
        hdr_tup = struct.unpack("<hhi", nxt)
        tgt = StrStruct(hdr_tup, st)
        raw = tgt.raw
        pos = 0
        parsed_data = dict()
        while pos + 4 < len(raw):
            rec_hdr = struct.unpack("<hh", raw[pos: pos + 4])
            rec_type_id = rec_hdr[0]
            rec_type = target_field_types[rec_type_id]
            rec_sz = rec_hdr[1]
            subst = raw[pos + 4: pos + 4 + rec_sz]
            parsed_data[rec_type] = subst.decode('utf-8', errors="ignore").replace("\x00", '')
            pos += 4 + rec_sz

        return parsed_data


def random_user_agent():
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/74.0.3729.169 Safari/537.36",
        "Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/60.0.3112.90 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0",
        "Mozilla/5.0 (Linux; Android 8.0.0; SM-G960F Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko)",
    ]

    return choice(user_agents)


def requests_retry_session(retries=3, backoff_factor=0.3, status_forcelist=(500, 502, 504), session=None):
    session = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session


# Need to make people don't give unicorns as an input
def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


# Verifies if the endpoint has authentication enabled and looks for NTLM specifically
def detect_ntlm_auth(url):
    if not is_valid_url(url):
        return False
    else:
        try:
            response = requests.head(url, verify=False, timeout=4)
        except Exception as e:
            print('[!] Error processing {} - '.format(url), e.__class__.__name__)
            return "FAIL " + str(e.__class__.__name__)

        else:
            if response.status_code == 401:
                response_headers = dict(response.headers)
                if 'WWW-Authenticate' in response_headers.keys():
                    if 'NTLM' in response_headers['WWW-Authenticate']:
                        print("[+] {} has NTLM authentication enabled".format(url))
                        return True
                    else:
                        print("[+] {} requires authentication but the method was found to be {}".format(
                            url, response_headers['WWW-Authenticate']
                        ))
            else:
                return False


def gather_ntlm_info(url):
    # Let's validate if it's a URL first
    if not is_valid_url(url):
        return False
    else:
        response_data = dict()
        response_data[url] = dict()
        response_data[url]['meta'] = dict()

        ntlm_check_response = detect_ntlm_auth(url)
        if ntlm_check_response:
            if type(ntlm_check_response) is not bool:
                if 'FAIL ' in ntlm_check_response:
                    return False
            # Send a random auth header to get response with NTLMSSP data
            headers = {
                'Authorization' : 'NTLM TlRMTVNTUAABAAAAMpCI4gAAAAAoAAAAAAAAACgAAAAGAbEdAAAADw=='
            }
            response_data[url]['meta']['is_valid_url'] = True
            response_data[url]['meta']['has_ntlm_endpoint'] = True
            auth_response = requests_retry_session().get(url, verify=False, headers=headers)
            auth_header = dict(auth_response.headers)
            if 'WWW-Authenticate' in auth_header.keys():
                response_data[url]['meta']['has_authenticate_header'] = True
                header_data = auth_header['WWW-Authenticate']
                try:
                    ntlm_string = header_data.split(',')[0][5:]
                except:
                    print("Error parsing NTLM string for {}. Please check manually!".format(url))
                else:
                    server_details = decode_ntlm_str(ntlm_string)
                    if server_details:
                        response_data[url]['meta']['status'] = 'ok'
                        response_data[url]['data'] = server_details
                        # Let's save some bytes
                        del (response_data[url]['data']['UNKNOWN'])
                        """
                        if 'ews' in url:
                            response_data[url]['data']['Server Type'] = 'Exchange Web Application'
                        elif 'iwa_test' in url:
                            response_data[url]['data']['Server Type'] = 'Okta IWA'
                        """
                        return response_data
                    else:
                        """
                        response_data[url]['meta']['status'] = 'fail'
                        response_data[url]['meta']['reason'] = 'NTLM decode failed'
                        return response_data
                        """
                        return False

            else:
                return False
                """
                response_data[url]['meta']['has_authenticate_header'] = False
                response_data[url]['meta']['status'] = 'fail'
                response_data[url]['meta']['reason'] = 'WWW-Authenticate header not found. Headers - {}'.format(
                    str(auth_header))
                return response_data
                """

        else:
            print("[!] No NTLM authentication endpoint found at {}".format(url))
            return False
