from iptools import IpRangeList
import sys
import re
import random


CIDR_REGEX = "^([0-9]{1,3}\.){3}[0-9]{1,3}(\/([0-9]|[1-2][0-9]|3[0-2]))?$"
URL_REGEX = "^(?:http(s)?:\/\/)?[\w.-]+(?:\.[\w\.-]+)+[\w\-\._~:/?#[\]@!\$&'\(\)\*\+,;=.]+$"
HOST_REGEX = "^(([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\-]*[a-zA-Z0-9])\.)*" \
             "([A-Za-z0-9]|[A-Za-z0-9][A-Za-z0-9\-]*[A-Za-z0-9])$"


def _cidr_to_iplist(cidr):
    try:
        ip_range = IpRangeList(cidr)
        return list(ip_range)
    except TypeError:
        print("[!] That's not a valid IP address or CIDR")
        return False


def _identify_and_return_records(inputstr, shuffle=False):
    master_records = []

    if re.match(CIDR_REGEX, inputstr):
        # Get results and add https prefix to it and pass it to master records
        iplist = ["https://" + str(x) for x in _cidr_to_iplist(inputstr)]
        master_records.extend(iplist)
    # Keep in intact after adding http prefix for all URL_REGEX URLs
    elif re.match(URL_REGEX, inputstr):
        if inputstr.startswith("http://") or inputstr.startswith("https://"):
            master_records.append(inputstr)
        else:
            master_records.append("https://" + str(inputstr))
    elif re.match(HOST_REGEX, inputstr):
        master_records.append("https://" + str(inputstr))

    if shuffle:
        random.shuffle(master_records)
        return master_records
    else:
        return master_records


def readfile_and_gen_input(file, shuffle=False):
    master_records = []
    try:
        with open(file, 'r') as fr:
            lines = fr.read().split('\n')
    except FileNotFoundError:
        print("[!] Input file specified by you does not exist. Please check file path and location")
        sys.exit()
    except OSError:
        print("[!] Unable to open the file. Please check file path and permissions!")
        sys.exit()
    else:
        for line in lines:
            if not line:
                continue
            else:
                master_records.extend(_identify_and_return_records(line, shuffle))

        return master_records


def read_input_and_gen_list(inputstr, shuffle=False):
    master_records = []
    master_records.extend(_identify_and_return_records(inputstr, shuffle))
    return master_records
