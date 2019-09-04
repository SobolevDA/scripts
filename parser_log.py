#!/usr/bin/python3.4
import re
import os

blacklist = open('/opt/provider/conntrack_limit/blacklist_connlimit.lst').read()


def ip_search():
    data = open('/var/log/conntrack_limit.log').read()
    pattern_ip = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\t\d{4,6}'
    pattern_blacklist = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
    ips = re.findall(pattern_ip, data)
    black = re.findall(pattern_blacklist, blacklist)
    for ip in ips:
        result = re.split(r'\t', ip)
        if int(result[1]) > 10000:
            if result[0] in black:
                print("Ipaddress already added")
            else:
                os.system("echo {} >> /opt/provider/conntrack_limit/blacklist_connlimit.lst".format(result[0]))
                print("Ipaddres add")


ip_search()
