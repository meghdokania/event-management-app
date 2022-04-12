import smtplib
from email.mime.text import MIMEText

smtp_ssl_host = 'smtp.gmail.com'
smtp_ssl_port = 465
username = 'prastuti@iitbhu.ac.in'
password = 'PASSWORD_FOR_prastuti@iitbhu.ac.in'
sender = 'himanshubb.eee18@itbhu.ac.in'
targets = ['paneertikka09@gmail.com', 'himanshubalasamanta@gmail.com']

msg = MIMEText('Hi, how are you today?')
msg['Subject'] = 'Hello'
msg['From'] = sender
msg['To'] = ', '.join(targets)

server = smtplib.SMTP_SSL(smtp_ssl_host, smtp_ssl_port)
server.login(username, password)
server.sendmail(sender, targets, msg.as_string())
server.quit()