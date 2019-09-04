import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import os

addr_from = "example@mail.ru"
password = "Password"
addr_to = "example_to@mail.ru"

msg = MIMEMultipart()
msg['From'] = addr_from
msg['To'] = addr_to
msg['Subject'] = "Example"

body = "Theme mail"
msg.attach(MIMEText(body, 'plain'))

filepatch = "/path/to/file/name.xls"
filename = os.path.basename(filepatch)

fp = open(filepatch, 'rb')
files = MIMEApplication(fp.read(), _subtype='xls')
fp.close()
files.add_header('Content-Disposition', 'attachment', filename=filename)
msg.attach(files)

server = smtplib.SMTP('mail.server.com', 25)
#server.set_debuglevel(True)
#server.starttls()
server.login(addr_from, password)
server.send_message(msg)
server.quit()
