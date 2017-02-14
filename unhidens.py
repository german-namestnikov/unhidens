#!/usr/bin/python3

import subprocess
import json
import socket
import argparse

REQUESTS_PER_NS = 25

def get_ns(domain):
    out = ""
    out = subprocess.check_output(['dig', domain, '-t', 'ns', '+short'])
    return out.decode('ascii').rstrip().split('\n')

def get_real_name(ns):
    out = ""
    ns = '@' + ns
    out = subprocess.check_output(['dig', ns, 'hostname.bind.', 'txt', 'chaos', '+short'])
    out = out.decode('ascii').rstrip().replace('"','')
   
    return out

def get_version(ns):
    out = ""
    ns = '@' + ns
    out = subprocess.check_output(['dig', ns, 'version.bind.', 'txt', 'chaos', '+short'])
    out = out.decode('ascii').rstrip().replace('"','')

    return out

def get_ip(name, domain = ''):
    try:
        ip = socket.gethostbyname(name)
    except Exception as e:
        try:
            if domain:
                ip = socket.gethostbyname(name + '.' + domain)
            else:
                ip = ''
        except Exception as e:
            ip = ''

    return ip

def verbose(comment):
    if args.verbose:
        print(comment)

parser = argparse.ArgumentParser(description="Small utility exploiting DNS Chaosnet TXT requests to obtain information about servers placed behind load balancers, firewalls and other.")
parser.add_argument("--domain", help="Select domain for NS enumeration.")
parser.add_argument("--verbose", help = "Show additional info about script flow.", action="store_true")

args = parser.parse_args()
if not args.domain:
    parser.print_help()
    exit()

ns_list = get_ns(args.domain)
verbose("; Found next NS for domain '%s': %s" % (args.domain, str(ns_list)))
verbose("")

ns_dict = dict()

for ns in ns_list:
    verbose("; Work started for NS '%s'" % (ns))
    real_names_list = []
    real_versions_list = []
    try:
        for i in range(REQUESTS_PER_NS):
            real_name = get_real_name(ns)
            real_ip = get_ip(real_name, args.domain)
            
            real_version = get_version(ns)            
            if real_version not in real_versions_list:
                real_versions_list.append(real_version)
            
            ns_record = {'name': real_name, 'ip': real_ip}
            if ns_record not in real_names_list:
                real_names_list.append(ns_record)
        
        ns_ip = get_ip(ns)
        verbose("; Found next servers for given NS '%s' (%s): %s" % (ns, ns_ip, str(real_names_list)))
        verbose("; Associated versions: %s" % (str(real_versions_list)))
        verbose("")
        ns_dict[ns] = {'ip': ns_ip, 'servers': real_names_list, 'versions': real_versions_list}

    except Exception as e:
        break
 
if args.verbose:
    comment = "; Final results in JSON:"
    print(comment)   

print(json.dumps(ns_dict, indent=4, sort_keys=True))

