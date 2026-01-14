from flask import render_template
import smtplib
from dotenv import load_dotenv
import os
import email.mime
import ssl

load_dotenv()
mail_restaurant = os.getenv('MAIL_USERNAME')
mail_pass = os.getenv('MAIL_PASSWORD')

def send_email_notification(recipient_email, data):
    msg = email.mime.MIMEMultipart()
    msg['From'] = mail_restaurant
    msg['To'] = recipient_email