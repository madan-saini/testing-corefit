
from smtplib import SMTP 
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import os

def send_mail(to, subject, bodyContent):
    # print(to)
    to_email = to
    from_email = 'sumit@nimbleappgenie.com'
    subject = subject
    message = MIMEMultipart()
    message['Subject'] = subject
    message['From'] = from_email
    message['To'] = to_email

    message.attach(MIMEText(bodyContent, "html"))
    msgBody = message.as_string()

    server = SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(from_email, 'Nimble@46')
    server.sendmail(from_email, to_email, msgBody)

    server.quit()