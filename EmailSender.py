import logging
import os
import smtplib
import sys

from email.mime.text import MIMEText
from email.header import Header
from configparser import ConfigParser

from docx import Document


class EmailSender:
    def __init__(self, file_config):
        self.base_path = os.path.dirname(os.path.abspath(__file__))
        self.config_path = os.path.join(self.base_path, file_config)
        if os.path.exists(self.config_path):
            self.cfg = ConfigParser()
            self.cfg.read(self.config_path, encoding='utf-8')
        else:
            logging.error("Config not found! Exiting!")
            sys.exit(1)

    def run(self):
        """
        Method run to send emails
        """
        subject = self.cfg.get("emails", "subject")
        emails = self.cfg.get("emails", "to")
        body_text = ""
        document = Document('./report.docx')

        for para in document.paragraphs:
            body_text += para.text + '\n'

        for email in emails.split(', '):
            self.send_email(subject, body_text, email)

    def send_email(self, subject, body_text, email):
        """
        Send email to a specific recipient
        Args:
            subject (str): Subject of the email
            body_text (str): Body text of the email
            email (str): Email address of the recipient
        """

        host = self.cfg.get("smtp", "server")
        login, passwd = self.cfg.get("smtp", "login"), self.cfg.get("smtp", "passwd")
        from_addr = self.cfg.get("smtp", "from_addr")

        msg = MIMEText(body_text, 'plain')
        msg['Subject'] = Header(subject)
        msg['From'] = from_addr
        msg['To'] = email

        server = smtplib.SMTP_SSL(host)
        server.login(login, passwd)
        server.set_debuglevel(1)
        server.sendmail(msg['From'], msg['To'], msg.as_string())
