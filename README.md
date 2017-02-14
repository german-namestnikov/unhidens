# Unhidens
#### usage: unhidens.py [-h] [--domain DOMAIN] [--verbose]

Small utility exploiting DNS Chaosnet TXT requests to obtain information about
servers placed behind load balancers, firewalls and other.

Requires 'dig' utility!

optional arguments:
  -h, --help       show this help message and exit
  --domain DOMAIN  Select domain for NS enumeration.
  --verbose        Show additional info about script flow.
