#!/usr/bin/env python3

import os
import argparse
import requests

from ipaddress import IPv4Address, IPv4Network


def scan_host(ip, port):
    identify_string = '<title>Solr Admin</title>'
    r = None
    timeout = 0.5
    try:
        url = 'http://{0}:{1}/solr/#/~cores/'.format(ip, port)
        r = requests.get(url, timeout=timeout)
    except Exception:
        pass
    try:
        url = 'https://{0}:{1}/solr/#/~cores/'.format(ip, port)
        r = requests.get(url, timeout=timeout)
    except Exception:
        pass

    if r and identify_string in r.text:
        print('{0} is unauthenticated'.format(url))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', metavar='192.0.2.1 / targets.txt', help='host to scan, or line separated file', required=True)
    parser.add_argument('-p', metavar='8983', default=8983, help='port(s) to scan, comma separated', required=False)
    parser.add_argument('-v', action='store_true', help='verbose, show each scan item', required=False)
    args = parser.parse_args()

    targets = []
    ports = str(args.p).split(',')

    try:
        if '/' in args.t:
            for ip in list(IPv4Network(args.t, strict=False).hosts()):
                targets.append(ip)
        else:
            targets.append(IPv4Address(args.t))
    except Exception:
        pass
    if not targets and os.path.isfile(args.t):
        with open(args.t, 'r') as f:
            lines = f.readlines()
            for line in lines:
                if '/' in line.strip():
                    try:
                        for ip in list(IPv4Network(line.strip(), strict=False).hosts()):
                            targets.append(ip)
                    except Exception:
                        pass
                else:
                    try:
                        targets.append(IPv4Address(line.strip()))
                    except Exception:
                        pass

    if not len(targets):
        print('Unable to read target information')
        exit()
    elif not len(ports):
        print('Unable to read port information')
        exit()

    for target in targets:
        for port in ports:
            if args.v:
                print('scanning {0}:{1}'.format(target, port))
            scan_host(str(target), port)


if __name__ == '__main__':
    main()
