[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com)
  [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) [![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://GitHub.com/sachinkamath/ntlmrecon/graphs/commit-activity)

 
# NTLMRecon

A fast and flexible NTLM reconnaissance tool without external dependencies. Useful to find out information about NTLM endpoints when working with a large set of potential IP addresses and domains.


NTLMRecon is built with flexibilty in mind. Need to run recon on a single URL, an IP address, an entire CIDR range or combination of all of it all put in a single input file? No problem! NTLMRecon got you covered. Read on.


# Demo

[![asciicast](https://asciinema.org/a/e4ggPBbzpJj9cIWRwK67D8xnw.svg)](https://asciinema.org/a/e4ggPBbzpJj9cIWRwK67D8xnw)

# TODO

1. Implement aiohttp based solution for sending requests
2. Integrate a spraying library
3. Add other authentication schemes found to the output
4. Automatic detection of autodiscover domains if domain


# Overview

NTLMRecon looks for NTLM enabled web endpoints, sends a fake authentication request and enumerates the following information from the NTLMSSP response:

1. AD Domain Name 
2. Server name
3. DNS Domain Name
4. FQDN
5. Parent DNS Domain

Since NTLMRecon leverages a python implementation of NTLMSSP, it eliminates the overhead of running Nmap NSE `http-ntlm-info` for every successful discovery.

On every successful discovery of a NTLM enabled web endpoint, the tool enumerates and saves information about the domain as follows to a CSV file :


| URL                      	| Domain Name 	| Server Name 	| DNS Domain Name   	| FQDN                         	| DNS Domain  	|
|--------------------------	|-------------	|-------------	|-------------------	|------------------------------	|-------------	|
| https://contoso.com/EWS/ 	| XCORP       	| EXCHANGE01  	| xcorp.contoso.net 	| EXCHANGE01.xcorp.contoso.net 	| contoso.net 	|

# Installation


### BlackArch

NTLMRecon is already packaged for BlackArch and can be installed by running `pacman -S ntlmrecon`

### Arch 

If you're on Arch Linux or any Arch linux based distribution, you can grab the latest build from the [Arch User Repository](https://aur.archlinux.org/packages/ntlmrecon/).

### PyPI

You can simply run `pip install ntlmrecon` to fetch the latest build from [PyPI](https://pypi.org/project/ntlmrecon/)

### Build from source

1. Clone the repository             : `git clone https://github.com/sachinkamath/ntlmrecon/`
2. RECOMMENDED - Install virtualenv : `pip install virtualenv`
3. Start a new virtual environment  : `virtualenv venv` and activate it with `source venv/bin/activate`
4. Run the setup file               : `python setup.py install`
5. Run ntlmrecon                    : `ntlmrecon --help`


# Usage

<pre>

 $ ntlmrecon --help                                                                                                                                                                                                                                 

         _   _ _____ _     ___  _________                     
        | \ | |_   _| |    |  \/  || ___ \                    
        |  \| | | | | |    | .  . || |_/ /___  ___ ___  _ __  
        | . ` | | | | |    | |\/| ||    // _ \/ __/ _ \| '_ \ 
        | |\  | | | | |____| |  | || |\ \  __/ (_| (_) | | | |
        \_| \_/ \_/ \_____/\_|  |_/\_| \_\___|\___\___/|_| |_|

             v.0.2 beta - Y'all still exposing NTLM endpoints?


usage: ntlmrecon [-h] [--input INPUT | --infile INFILE] [--wordlist WORDLIST] [--threads THREADS] [--output-type] [--outfile OUTFILE] [--random-user-agent] [--force-all] [--shuffle] [-f]

optional arguments:
  -h, --help           show this help message and exit
  --input INPUT        Pass input as an IP address, URL or CIDR to enumerate NTLM endpoints
  --infile INFILE      Pass input from a local file
  --wordlist WORDLIST  Override the internal wordlist with a custom wordlist
  --threads THREADS    Set number of threads (Default: 10)
  --output-type, -o    Set output type. JSON (TODO) and CSV supported (Default: CSV)
  --outfile OUTFILE    Set output file name (Default: ntlmrecon.csv)
  --random-user-agent  TODO: Randomize user agents when sending requests (Default: False)
  --force-all          Force enumerate all endpoints even if a valid endpoint is found for a URL (Default : False)
  --shuffle            Break order of the input files
  -f, --force          Force replace output file if it already exists


</pre>


## Example Usage

### Recon on a single URL

` $ ntlmrecon --input https://mail.contoso.com --outfile ntlmrecon.csv`

### Recon on a CIDR range or IP address

` $ ntlmrecon --input 192.168.1.1/24 --outfile ntlmrecon-ranges.csv`

### Recon on an input file

The tool automatically detects the type of input per line and gives you results automatically. CIDR ranges are expanded automatically even when read from a text file.

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

# Acknowledgements

* [@nyxgeek](https://github.com/nyxgeek) for the idea behind [ntlmscan](https://github.com/nyxgeek/ntlmscan).

# Feedback

If you'd like to see a feature added into the tool or something doesn't work for you, please open a new [issue](https://github.com/sachinkamath/ntlmrecon/issues/new).
