#!/usr/bin/python

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

parser = argparse.ArgumentParser(description="Small DNS Recon utility, allows you to obtain some useful info about NS-servers placed behind relays, firewalls, etc.")
parser.add_argument("--domain", help="Investigate all NS for a given domain.")
parser.add_argument("--server", help="Investigate only this NS.")
parser.add_argument("--verbose", help = "Show additional info about script flow.", action="store_true")

args = parser.parse_args()
if not args.domain and not args.server:
    parser.print_help()
    exit()

if args.domain:
    ns_list = get_ns(args.domain)
    verbose("; Found next NS for domain '%s': %s" % (args.domain, str(ns_list)))
    verbose("")
else:
    if args.server:
        ns_list = [args.server]


ns_dict = dict()
    
for ns in ns_list:
    verbose("; Work started for NS '%s'" % (ns))
    real_names_list = []
    real_versions_list = []
    
    for i in range(REQUESTS_PER_NS):
        try:
            real_name = get_real_name(ns)
            real_ip = get_ip(real_name, args.domain)
            
            real_version = get_version(ns)            
            if real_version and real_version not in real_versions_list:
                real_versions_list.append(real_version)
            
            ns_record = {'name': real_name, 'ip': real_ip}
            if real_name and ns_record not in real_names_list:
                real_names_list.append(ns_record)
 
        except Exception as e:
            if args.verbose:
                comment = "; " + str(e)
                print(comment)
            break
       
    ns_ip = get_ip(ns)
    verbose("; Found next servers for given NS '%s' (%s): %s" % (ns, ns_ip, str(real_names_list)))
    verbose("; Associated versions: %s" % (str(real_versions_list)))
    verbose("")
    ns_dict[ns] = {'ip': ns_ip, 'servers': real_names_list, 'versions': real_versions_list}

 
if args.verbose:
    comment = "; Final results in JSON:"
    print(comment)   

print(json.dumps(ns_dict, indent=4, sort_keys=True))

