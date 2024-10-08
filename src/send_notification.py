import ssl
import smtplib
import base64
from email.mime.text import MIMEText

def send_notification(subject="Experiment Notification", message="This email was sent automatically by code"):
    
    f=open("pass.txt", "r")
    lines = f.readlines()
    send_to = base64.b64decode(lines[1]).decode("utf-8")
    send_from = base64.b64decode(lines[2]).decode("utf-8")
    password = base64.b64decode(lines[0]).decode("utf-8")
    f.close()

    em = MIMEText(message)
    em['From'] = send_from
    em['To'] = send_to
    em['Subject'] = subject
    
    context = ssl.create_default_context()
    
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(send_from, password)
            smtp.sendmail(send_from, send_to, em.as_string())
    except Exception as e:
        print(e)
        print("Error: unable to send email")

if __name__ == "__main__":
    send_notification()