# NTLMRecon

A fast NTLM reconnaissance tool without external dependencies. Useful to find out information about NTLM endpoints when working with a large set of potential IP addresses and domains.

> Work in Progess. Things may break and change often.

NTLMRecon is built with flexibilty in mind. Need to run recon on a single URL, an IP address, an entire CIDR range or combination of all of it all put in a single input file? No problem! NTLMRecon got you covered. Read on.

Internal wordlists are from the awesome [nyxgeek/lyncsmash](https://github.com/nyxgeek/lyncsmash) repo

# Overview

NTLMRecon looks for NTLM enabled web endpoints, sends a fake authentication request and enumerates the following information from the NTLMSSP response:

1. AD Domain Name 
2. Server name
3. DNS Domain Name
4. FQDN
5. Parent DNS Domain

Since ntlmrecon leverages a python implementation of NTLMSSP, it eliminates the overhead of running Nmap NSE `http-ntlm-info` for every successful discovery.


# Installation

## Arch 

If you're on Arch Linux or any Arch linux based distribution, you can grab the latest build from [AUR](https://aur.archlinux.org/packages/ntlmrecon/)

## Generic Installation

1. Clone the repository - `git clone https://github.com/sachinkamath/ntlmrecon/`
2. RECOMMENDED - Install virtualenv `pip install virtualenv`
3. Start a new virtual environment - `virtualenv venv` and activate it with `source venv/bin/activate`
4. Run the setup file - `python setup.py install`
5. Run ntlmrecon - `ntlmrecon --help`


# Usage

<pre>


         _   _ _____ _     ___  _________
        | \ | |_   _| |    |  \/  || ___ \
        |  \| | | | | |    | .  . || |_/ /___  ___ ___  _ __
        | . ` | | | | |    | |\/| ||    // _ \/ __/ _ \| '_ \
        | |\  | | | | |____| |  | || |\ \  __/ (_| (_) | | | |
        \_| \_/ \_/ \_____/\_|  |_/\_| \_\___|\___\___/|_| |_|

             v.0.1 beta - Y'all still exposing NTLM endpoints?

usage: ntlmrecon [-h] [--input INPUT | --infile INFILE] [--wordlist WORDLIST] [--threads THREADS] [--output-type] --outfile OUTFILE [--random-user-agent] [--force-all] [--shuffle]

optional arguments:
  -h, --help           show this help message and exit
  --input INPUT        Pass input as an IP address, URL or CIDR to enumerate NTLM endpoints
  --infile INFILE      Pass input from a local file
  --wordlist WORDLIST  Override the internal wordlist with a custom wordlist
  --threads THREADS    Set number of threads (Default: 10)
  --output-type, -o    Set output type. JSON and CSV supported (Default: CSV) (TODO: JSON)
  --outfile OUTFILE    Set output file name (Default: ntlmrecon.csv)
  --random-user-agent  TODO: Randomize user agents when sending requests (Default: False) (TODO)
  --force-all          Force enumerate all endpoints even if a valid endpoint is found for a URL (Default : False)
  --shuffle            Break order of the input files (TODO: Improve logic)

</pre>


## Example Usage

### Recon on a single URL

` $ ntlmrecon --input https://mail.contoso.com --outfile ntlmrecon.csv`

### Recon on a CIDR range or IP address

` $ ntlmrecon --input 192.168.1.1/24 --outfile ntlmrecon-ranges.csv`

### Recon on an input file

NTLM recon automatically detects the type of input per line and gives you results automatically.
CIDR ranges are expanded automatically even when read from a text file.

Input file can be something as mixed up as :

<pre>
mail.contoso.com
CONTOSOHOSTNAME
10.0.13.2/28
192.168.222.1/24
https://mail.contoso.com
</pre>

To run recon with an input file, just run :

`$ ntlmrecon --infile /path/to/input/file --outfile ntlmrecon-fromfile.csv`

# Feedback

If you'd like to see a feature added into the tool or something doesn't work for you, please open a new [issue](https://github.com/sachinkamath/ntlmrecon/issues/new)
