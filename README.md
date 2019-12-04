# NTLMRecon
A fast NTLM reconnaissance tool without external dependencies written. Written for red teams <3

> Work in Progess. Thinks may break and change at anytime

NTLMRecon is built with flexibilty in mind. Need to run recon on a single URL, an IP address, an entire CIDR range or combination of all of it all put in a single input file?

No problem! NTLMRecon got you covered. Read on.


# Getting Started

1. Clone the repository - `git clone https://github.com/sachinkamath/pandora/`
2. RECOMMENDED - Install virtualenv `pip install virtualenv`
3. Start a new virtual environment - `virtualenv venv` and activate it with `source venv/bin/activate`
4. Run the setup file - `python setup.py install`
5. Run ntlmrecon - `ntlmrecon --help`


# Sneak peek

<pre>

usage: ntlmrecon [-h] [--input INPUT | --infile INFILE] [--threads THREADS] [--output-type] --outfile OUTFILE [--random-user-agent] [--force-all] [--shuffle]

Arguments:
  -h, --help           show this help message and exit
  --input INPUT        Pass input as an IP address, URL or CIDR to enumerate NTLM endpoints
  --infile INFILE      Pass input from a local file
  --threads THREADS    Set number of threads (Default: 10)
  --output-type, -o    Set output type. JSON (TODO) and CSV supported (Default: CSV)
  --outfile OUTFILE    Set output file name (Default: ntlmrecon.csv)
  --random-user-agent  TODO: Randomize user agents when sending requests (Default: False)
  --force-all          TODO: Force enumerate all endpoints even if a valid endpoint is found for a URL (Default : False)
  --shuffle            Break order of the input files
</pre>


# Example Usage

### Recon on a single URL

` $ ntlmrecon --input https://mail.contoso.com --outfile ntlmrecon.csv`

### Recon on a CIDR range or IP address

` $ ntlmrecon --input 192.168.1.1/24 --outfile ntlmrecon-ranges.csv`

### Recon on an input file

NTLM recon automatically detects the type of input per line and gives you results automatically.
CIDR ranges are expanded automatically even when read from a text file.

Input file can be something as complex as :

<pre>
mail.contoso.com
CONTOSOHOSTNAME
10.0.13.2/24
https://mail.contoso.com
</pre>

To run recon with an input file, just run :

`$ ntlmrecon --infile /path/to/input/file --outfile ntlmrecon-fromfile.csv`
