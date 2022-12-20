import sqlite3
from sqlite3 import Error

class User:
    def create_user(self, user_name: str, password:str, email:str) -> None:
        con = sqlite3.connect('sqldb_example.db')
        sql = "insert into User values ('{0}', '{1}','{2}')".format(user_name, password, email)
        con.execute(sql)
        con.commit()
        print('User registered with {username} and {password}')

import syslog

class Logger:
    def write_log_to_system(self, message: str) -> None:
        syslog.syslog(syslog.LOG_ERR, message)


import json
import smtplib, ssl 
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class Email:
    def send_email(self, to_email: str, message_content: str, subject='User Registered') -> None :
        with open('credentials.json') as f:
            data = json.load(f)
        smtp_server = "smtp.gmai.com"
        port = 465 
        sender_email = data["fromUser"]
        password = data['password']

        context = ssl.create_default_context()
        message = MIMEMultipart("alternative")

        message["From"] = sender_email
        message["To"] = to_email 
        message['Subject'] = subject
        message_content = f"Hello, <br/><b> New message: </b> <br/> \
        {message_content} <br/> Att,<br/> Leonardo Morelli Santos"

        part = MIMEText(message_content, "html")

        message.attach(part)

        with smtplib.SMTP_SSL(smtp_server,port,context=context) as server:
            server.login(sender_email,message.as_string())
        print("Mail sent to {to_email}")



class Registrations:
    def register_user(self, user_name: str, password:str, email: str) -> None:
        try:
            User().create_user(user_name, password, email)
            Email().send_email(email, 'User Registered!')
        except Exception:
            Logger().write_log_to_system('Error while registering user.')


r = Registrations()
r.register_user('Leonardo', '123456789', 'leonardo@email.com')
