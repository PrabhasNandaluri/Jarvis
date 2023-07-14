import smtplib
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

with open("Data\Input_Constants.Json") as f:
    constants = json.load(f)

def send_mail(subject: str, body: str, receiver: str) -> bool:
    success_msg: bool
    port = 587
    smtp_server = "smtp.gmail.com"
    sender_email = "j.e.f.f.bot.v.1@gmail.com"
    password = constants["email_password"]

    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = receiver

    part = MIMEText(body, "html")
    message.attach(part)

    try:
        mail = smtplib.SMTP(smtp_server, port)
        mail.ehlo()
        mail.starttls()
        mail.login("j.e.f.f.bot.v.1@gmail.com", password)
        mail.sendmail(sender_email, receiver, message.as_string())
        mail.quit()
        success_msg = True
    except smtplib.SMTPAuthenticationError:
        print("Invalid Credentials -> failed to send mail")
        success_msg = False
    except:
        print("Failed to send Mail")
        success_msg = False

    return success_msg

def log():
    pass
