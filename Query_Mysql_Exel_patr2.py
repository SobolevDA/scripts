import pymysql
import xlwt
from datetime import date, datetime
import dateutil.relativedelta

connections = pymysql.connect('localhost', 'User', 'password', 'database')
cursor = connections.cursor()

r_inet = 0
c_inet = 0
r_ktv = 0
c_ktv = 0 




end = date.today()
start = end - dateutil.relativedelta.relativedelta(months=1)
print(end, start)


def date_time(date):
    cursor.execute("select unix_timestamp('{}');".format(date))
    date = cursor.fetchall()
    return date[0][0]


date_end = date_time(end)
date_start = date_time(start)

wb = xlwt.Workbook()
ws_inet = wb.add_sheet("NameSheets {}-{}".format(start, end))
ws_ktv = wb.add_sheet("NameSheets_2 {}-{}".format(start, end))

service_inet = [97, 59, 58, 47, 50, 48, 46, 153, 49, 137]
service_ktv = [100, 99]


def search_customer_ethernet(d_start, d_end, id_cus):
    customer_discount = """select DISTINCT link_customer_service_id from discount 
                            where discount_time>{} 
                            and discount_time<{} 
                            and link_customer_service_id in (select id from link_customer_service where service_id={} 
                            and link_time<{} 
                            and unlink_time is NULL and is_deleted is NULL);""".format(d_start, d_end, id_cus, d_end)
    cursor.execute(customer_discount)
    customer_inet = cursor.fetchall()
    return customer_inet


def search_customer_ktv(id_ktv):
    cus_ktv = """select distinct  customer.id from customer, link_customer_service
                 where customer.id=link_customer_service.customer_id 
                 and customer.is_locked is NULL 
                 and customer.is_deleted is NULL 
                 and link_customer_service.is_deleted is NULL 
                 and link_customer_service.service_id={} and link_customer_service.unlink_time is NULL;""".format(id_ktv)
    cursor.execute(cus_ktv)
    customer_ktv = cursor.fetchall()
    return customer_ktv


for id_inet in service_inet:
    service_name = 'select name from service where id={}'.format(id_inet)
    cursor.execute(service_name)
    names = cursor.fetchall()
    
    customer_inet = search_customer_ethernet(date_start, date_end, id_inet)
    
    ws_inet.write(c_inet, 1, len(customer_inet))
    
    for name in names:
        ws_inet.write(r_inet, 0, name[0])
        r_inet += 1
    c_inet += 1

for id_ktv in service_ktv:
    service_name = 'select name from service where id={}'.format(id_ktv)
    
    cursor.execute(service_name)
    names = cursor.fetchall()

    customer_ktv = search_customer_ktv(id_ktv)

    ws_ktv.write(c_ktv, 1, len(customer_ktv))
    
    for name in names:
        ws_ktv.write(r_ktv, 0, name[0])
        r_ktv += 1
    c_ktv += 1

wb.save('/path/ti file/name.xls')
connections.close()

print("OK!")
