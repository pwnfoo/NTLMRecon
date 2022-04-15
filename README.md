[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com)
  [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) [![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://GitHub.com/sachinkamath/ntlmrecon/graphs/commit-activity)

 
# NTLMRecon

An NTLM reconnaissance tool without external dependencies. Useful to find out information about NTLM endpoints when working with a large set of potential IP addresses and domains.


NTLMRecon is built with flexibilty in mind. Need to run recon on a single URL, an IP address, an entire CIDR range or combination of all of it all put in a single input file? No problem! NTLMRecon got you covered. Read on.

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

### Build from source

1. Clone the repository             : `git clone https://github.com/pwnfoo/ntlmrecon/`
2. RECOMMENDED - Install virtualenv : `pip install virtualenv`
3. Start a new virtual environment  : `virtualenv venv` and activate it with `source venv/bin/activate`
4. Run the setup file               : `python setup.py install`
5. Run ntlmrecon                    : `ntlmrecon --help`

## Example Usage

### Recon on a single URL

` $ ntlmrecon --input https://mail.contoso.com --outfile ntlmrecon.csv`

### Recon on a CIDR range or IP address

` $ ntlmrecon --input 192.168.1.1/24 --outfile ntlmrecon-ranges.csv`

### Recon on an input file

The tool automatically detects the type of input per line and takes actions accordingly. CIDR ranges are expanded by default (please note that there is no de-duplication baked in just yet!)


P.S Handles a good mix like this well :

<pre>
mail.contoso.com
CONTOSOHOSTNAME
10.0.13.2/28
192.168.222.1/24
https://mail.contoso.com
</pre>

# TODO

1. Implement aiohttp based solution for sending requests
2. Integrate a spraying library
3. Add other authentication schemes found to the output
4. Automatic detection of autodiscover domains if domain

# Acknowledgements

* [@nyxgeek](https://github.com/nyxgeek) for the idea behind [ntlmscan](https://github.com/nyxgeek/ntlmscan).
