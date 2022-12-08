from conf.definitions import get_key
from email.message import EmailMessage
import ssl
import smtplib

def mail(receiver, subject, content):
    sender = 'info.equitramlve@gmail.com'
    password = get_key('data/mail.key')
    context = ssl.create_default_context()

    em = EmailMessage()
    em['From'] = sender
    em['To'] = receiver
    em['Subject'] = subject
    em.set_content(content)

    with smtplib.SMTP_SSL('smtp.gmail.com', '465', context = context) as smtp:
        smtp.login(sender, password)
        smtp.sendmail(sender, receiver, em.as_string())

def get_user_data():
    user = ""
    password = ""
    with open("data/database/email.db", "r") as f:
        file = f.readlines()
        user = file[0].strip()
        password = file[1].strip()

    return user, password

def send_newsletter(subject, content):
    email_list = []
    with open(r'data/database/newsletter.db', 'r') as f:
        for line in f:
            x = line[:-1]
            email_list.append(x)

    for element in email_list:
        mail(element, subject, content)