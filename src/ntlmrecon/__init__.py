import argparse
import json
import requests
import csv
import sys
import os

from colorama import init as init_colorama
from multiprocessing.dummy import Pool as ThreadPool
from ntlmrecon.ntlmutil import gather_ntlm_info
from ntlmrecon.misc import print_banner, INTERNAL_WORDLIST
from ntlmrecon.inpututils import readfile_and_gen_input, read_input_and_gen_list
from termcolor import colored
from urllib.parse import urlsplit

# Initialize colors in Windows - Because I like Windows too!
init_colorama()

# make the Pool of workers
# TODO: Make this an argument

FOUND_DOMAINS = []


def in_found_domains(url):
    split_url = urlsplit(url)
    if split_url.hostname in FOUND_DOMAINS:
        return True
    else:
        return False


def write_records_to_csv(records, filename):
    if os.path.exists(filename):
        append_write = 'a'
    else:
        append_write = 'w+'

    with open(filename, append_write) as file:
        writer = csv.writer(file)
        if append_write == 'w+':
            writer.writerow(['URL', 'AD Domain Name', 'Server Name', 'DNS Domain Name', 'FQDN', 'Parent DNS Domain'])
        for record in records:
            csv_record = list()
            url = list(record.keys())[0]
            csv_record.append(url)
            csv_record.extend(list(record[url]['data'].values()))
            writer.writerow(csv_record)


def main():
    # Init arg parser
    parser = argparse.ArgumentParser(description=print_banner())
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--input', '-i',  help='Pass input as an IP address, URL or CIDR to enumerate NTLM endpoints')
    group.add_argument('--infile', '-I', help='Pass input from a local file')
    parser.add_argument('--wordlist', help='Override the internal wordlist with a custom wordlist', required=False)
    parser.add_argument('--threads', help="Set number of threads (Default: 10)", required=False, default=10)
    parser.add_argument('--output-type', '-o', help='Set output type. JSON (TODO) and CSV supported (Default: CSV)',
                        required=False, default='csv', action="store_true")
    parser.add_argument('--outfile', '-O', help='Set output file name (Default: ntlmrecon.csv)', default='ntlmrecon.csv')
    parser.add_argument('--random-user-agent', help="TODO: Randomize user agents when sending requests (Default: False)",
                        default=False, action="store_true")
    parser.add_argument('--force-all', help="Force enumerate all endpoints even if a valid endpoint is found for a URL "
                                            "(Default : False)", default=False, action="store_true")
    parser.add_argument('--shuffle', help="Break order of the input files", default=False, action="store_true")
    parser.add_argument('-f', '--force', help="Force replace output file if it already exists", action="store_true",
                        default=False)
    args = parser.parse_args()

    if not args.input and not args.infile:
        print(colored("[!] How about you check the -h flag?", "red"))

    if os.path.isdir(args.outfile):
        print(colored("[!] Invalid filename. Please enter a valid filename!", "red"))
        sys.exit()
    elif os.path.exists(args.outfile) and not args.force:
        print(colored("[!] Output file {} already exists. "
                      "Choose a different file name or use -f to overwrite the file".format(args.outfile), "red"))
        sys.exit()

    pool = ThreadPool(int(args.threads))

    if args.input:
        records = read_input_and_gen_list(args.input, shuffle=args.shuffle)
    elif args.infile:
        records = readfile_and_gen_input(args.infile, shuffle=args.shuffle)
    else:
        sys.exit(1)

    # Check if a custom wordlist is specified
    if args.wordlist:
        try:
            with open(args.wordlist, 'r') as fr:
                wordlist = fr.read().split('\n')
                wordlist = [x for x in wordlist if x]
        except (OSError, FileNotFoundError):
            print(colored("[!] Cannot read the specified file {}. Check if file exists and you have "
                          "permission to read it".format(args.wordlist), "red"))
            sys.exit(1)
    else:
        wordlist = INTERNAL_WORDLIST
    # Identify all URLs with web servers running
    for record in records:
        print(colored("[+] Brute-forcing {} endpoints on {}".format(len(wordlist), record), "yellow"))
        all_combos = []
        for word in wordlist:
            if word.startswith('/'):
                all_combos.append(str(record+word))
            else:
                all_combos.append(str(record+"/"+word))

        results = pool.map(gather_ntlm_info, all_combos)
        results = [x for x in results if x]
        if results:
            write_records_to_csv(results, args.outfile)
            print(colored('[+] Output for {} saved to {} '.format(record, args.outfile), 'green'))



