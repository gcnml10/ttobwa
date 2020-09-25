import smtplib
from email.mime.text import MIMEText
google_server = smtplib.SMTP_SSL('smtp.gmail.com',465)
# google_server.starttls()
#
google_server.login('gcnml0@gmail.com','ejugnntzoqaeskkk')

send_email = 'ddddd'
msg = MIMEText('dddddddd')
msg['Subject'] ='dddddddddd'

google_server.sendmail(send_email,'gcnml0@gmail.com',msg.as_string())

google_server.quit()