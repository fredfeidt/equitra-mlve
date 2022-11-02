import smtplib
import ssl

def get_user_data():
    user = ""
    password = ""
    with open("data/database/email.db", "r") as f:
        file = f.readlines()
        user = file[0].strip()
        password = file[1].strip()

    return user, password

def mail(receiver, subject, content):
    sender, password = get_user_data()
    message = f"Subject: {subject}\n\n{content}"

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("mail.equitra-mlve.eu", 465, context=context) as server:
        server.login(sender, password)
        server.sendmail(sender, receiver, message)

def send_newsletter(subject, content):
    email_list = []
    with open(r'data/database/newsletter.db', 'r') as f:
        for line in f:
            x = line[:-1]
            email_list.append(x)

    for element in email_list:
        mail(element, subject, content)