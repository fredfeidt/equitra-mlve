from cryptography.fernet import Fernet
import shutil
import os
from PyPDF2 import PdfFileReader
from datetime import date, datetime

def newsletter(form, current_user, is_signed_up):
    email = current_user.email
    email_list = []

    if is_signed_up == False:
        with open(r'data/database/newsletter.db', 'r') as f:
            for line in f:
                x = line[:-1]
                email_list.append(x)
        if email not in email_list:
            email_list.append(email)
            with open(r'data/database/newsletter.db', 'w') as f:
                for item in email_list:
                    f.write("%s\n" % item)
    else:
        with open(r'data/database/newsletter.db', 'r') as f:
            for line in f:
                x = line[:-1]
                email_list.append(x)
        if email in email_list:
            email_list.remove(email)
            with open(r'data/database/newsletter.db', 'w') as f:
                for item in email_list:
                    f.write("%s\n" % item)

def generate_key():
    key = Fernet.generate_key()
    with open('data/app.key', 'w') as filekey:
        filekey.write(key)

def get_key(path):
    with open(path, 'r') as filekey:
        key = filekey.read()
        return key

def clear_folder(folder):
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

def pdf2article(path, filename):
    pdf = PdfFileReader(path)
    with open(f'data/articles/{filename}.txt', 'w') as f:
        for pageNum in range(pdf.numPages):
            pageObj = pdf.getPage(pageNum)

            try:
                txt = pageObj.extract_text()
                print(''.center(100, '-'))
            except:
                pass
            else:
                f.write(txt)

        f.close()

    # Make a list of all articles
    articles = []
    with open(r'data/database/articles.db', 'r') as f:
        for line in f:
            x = line[:-1]
            articles.append(x)

    articles.append(filename)
    with open(r'data/database/articles.db', 'w') as f:
        for item in articles:
            f.write("%s\n" % item)

def log(text):
    today = date.today()
    file = f"data/log/{today}.log"

    if os.path.exists(file):
        with open(f"data/log/{today}.log", "a") as log:
            current_time = datetime.now()
            time = current_time.strftime("%H:%M")
            log.write(f"{time} | {text}\n")
    else:
        f = open(f"data/log/{today}.log", "w")
        f.write(f"Log file | {today}\n\n")
        f.close()
        with open(f"data/log/{today}.log", "a") as log:
            current_time = datetime.now()
            time = current_time.strftime("%H:%M")
            log.write(f"{time} | {text}\n")