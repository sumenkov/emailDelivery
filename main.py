import os
import smtplib
import sys

from datetime import datetime
from email.mime.text import MIMEText
from email.header import Header
from configparser import ConfigParser
from docx import Document

base_path = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(base_path, "config.ini")
if os.path.exists(config_path):
    cfg = ConfigParser()
    cfg.read(config_path, encoding='utf-8')
else:
    print("Config not found! Exiting!")
    sys.exit(1)
    

def main():
    subject = cfg.get("emails", "subject")
    emails = cfg.get("emails", "to")
    body_text = ""
    document = Document('./report.docx')

    for para in document.paragraphs:
        body_text += para.text + '\n'

    for email in emails.split(', '):
        send_email(subject, body_text, email)


def send_email(subject, body_text, email):
    """
    Отправить email
    """
    host = cfg.get("smtp", "server")
    login, passwd = cfg.get("smtp", "login"), cfg.get("smtp", "passwd")
    from_addr = cfg.get("smtp", "from_addr")

    msg = MIMEText(body_text, 'plain')
    msg['Subject'] = Header(subject)
    msg['From'] = from_addr
    msg['To'] = email

    server = smtplib.SMTP_SSL(host)
    server.login(login, passwd)
    server.set_debuglevel(1)
    server.sendmail(msg['From'], msg['To'], msg.as_string())


if __name__ == '__main__':
    main()
