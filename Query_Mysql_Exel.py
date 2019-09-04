import pymysql
import xlwt
import wget

connections = pymysql.connect('localhost', 'user', 'password', 'database')
cursor = connections.cursor()

street_id = [93, 3, 4, 97, 89, 47, 59, 5, 46, 94, 9, 2, 92, 98, 96, 91, 6, 7, 95, 90]
service_id = {100: 200, 99: 59}

i = 0

wb = xlwt.Workbook()
ws = wb.add_sheet('Name Sheets')

for streets in street_id:
    for services in service_id:
        query_sql = 'select distinct customer.name, customer.id, street.name, address.house, address.appart, service.name, customer.balance ' \
                    'from street,service, customer,address,link_customer_service ' \
                    'where customer.address_id=address.id and address.street_id={} and street.id={} ' \
                    'and link_customer_service.service_id={} and service.id={} ' \
                    'and link_customer_service.unlink_time is NULL ' \
                    'and customer.id=link_customer_service.customer_id and customer.balance <-{} ' \
                    'and customer.is_locked  is NULL and customer.is_deleted is NULL;'.format(streets, streets, services, services, service_id[services])

        cursor.execute(query_sql)
        data = cursor.fetchall()

        sort = sorted(data, key=lambda x: x[3])
        for x in sort:
            ws.write(i, 0, x[0])
            ws.write(i, 1, x[1]+793000)
            ws.write(i, 2, x[2])
            ws.write(i, 3, x[3])
            ws.write(i, 4, x[4])
            ws.write(i, 5, x[5])
            ws.write(i, 6, x[6])
            i += 1
       
wb.save('/path/to/file/name.xls')
connections.close()

#url = "/home/hmirin/python_virtual_mash/sheets/Должники КТВ.xls"
#wget.download(url)
