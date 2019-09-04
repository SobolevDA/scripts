import pymysql
import re

connections = pymysql.connect('localhost',
                              'root',
                              '',
                              'provider')
cursor = connections.cursor()

blacklist = open('blacklist_connlimit.lst').read()

pattern_blacklist = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
black = re.findall(pattern_blacklist, blacklist)
out_info = []

for ipaddr in black:
    addr = "select distinct customer.name, street.name, address.house, address.appart"\
    " from street, customer, address, ip_customer "\
    "where customer.address_id=address.id and ip_customer.customer_id=customer.id "\
    " and address.street_id=street.id and ip_customer.ip=inet_aton('{}') "\
    "and ip_customer.mask=inet_aton('255.255.255.252') and customer.is_locked  is NULL and customer.is_deleted is NULL;".format(ipaddr)

    cursor.execute(addr)
    customer = cursor.fetchall()
    for address in customer:
        out_info.append(address)

bad_ip = open('bad_ip.txt', 'w')
for i in out_info:
    bad_ip.write(i[0] + ' ' + i[1] + ' ' + str(i[2]) + ' ' + str(i[3]) + '\n')
connections.close()
