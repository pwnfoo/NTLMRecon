import argparse
import json
import requests

from colorama import init as init_colorama
from multiprocessing.dummy import Pool as ThreadPool
from ntlmrecon.ntlmutil import gather_ntlm_info
from ntlmrecon.misc import print_banner
from ntlmrecon.inpututils import readfile_and_gen_input, read_input_and_gen_list
from termcolor import colored

# Initialize colors in Windows - Because I like Windows too!
init_colorama()


# make the Pool of workers
# TODO: Make this an argument
#pool = ThreadPool(16)

#results = pool.map(gather_ntlm_info, urls)


def main():
    # Init arg parser
    parser = argparse.ArgumentParser(description=print_banner())
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--input', help='Pass input as an IP address, URL or CIDR to enumerate NTLM endpoints')
    group.add_argument('--infile', help='Pass input from a local file')
    # parser.add_argument('--wordlist', help='Override the internal wordlist with a custom wordlist', required=False)
    parser.add_argument('--threads', help="Set number of threads (Default: 10)", required=False, default=10)
    parser.add_argument('--output-type', '-o', help='Set output type. JSON and CSV supported (Default: CSV)',
                        required=False, default='csv', action="store_true")
    parser.add_argument('--outfile', help='Set output file name (Default: ntlmrecon.csv)', required=True)
    parser.add_argument('--random-user-agent', help="Randomize user agents when sending requests (Default: False)",
                        default=False, action="store_true")
    parser.add_argument('--shuffle', help="Shuffle the targets randomly to prevent "
                                          "consecutive requests (Default: False)", default=False, action="store_true")
    parser.add_argument('--force-all', help="Force enumerate all endpoints even if a valid endpoint is found for a URL "
                                            "(Default : False)", default=False, action="store_true")

    args = parser.parse_args()

    if args.input:
        if args.shuffle:
            records = read_input_and_gen_list(args.input, shuffle=True)
        else:
            records = read_input_and_gen_list(args.input, shuffle=False)
    elif args.infile:
        if args.shuffle:
            records = readfile_and_gen_input(args.infile, shuffle=True)
        else:
            records = readfile_and_gen_input(args.infile, shuffle=False)

    print(records)


#(json.dumps(results))
# close the pool and wait for the work to finish
#pool.close()
#pool.join()

