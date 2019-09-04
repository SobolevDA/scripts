import telnetlib
from easysnmp import snmp_get
import re
from os import system
from ipaddress import IPv4Address
import time


first_ip = IPv4Address('192.168.1.1')
last_ip = IPv4Address('192.168.1.50')
system_name = '.1.3.6.1.2.1.1.5.0'
dhcp_server = '192.168.50.1'
com = 'public'
ver = 2

while last_ip >= first_ip:
    response = system("ping -c 3 {}".format(first_ip))
    if response == 0:
        snmp_name = snmp_get(system_name, hostname=str(first_ip), community=com, version=ver)
        pattern_snmp = r'\d{4}'
        switch_name = re.findall(pattern_snmp, snmp_name.value)
        tn = telnetlib.Telnet(str(first_ip), 23, 2)
        tn.read_until(b'UserName:')
        tn.write(b'\n')
        tn.read_until(b'PassWord:')
        tn.write(b'\n')
        tn.write(b'enable rmon\n')
        #tn.write(b'config dhcp_relay add vlanid %s 192.168.50.1\n' % switch_name[0].encode())
        tn.write(b'save\n')
        time.sleep(3)
        tn.write((b'logo\n'))
        tn.close()
        print("Rmon enabled")
    else:
        print("Host is down")

    first_ip += 1

