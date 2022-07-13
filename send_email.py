from email.base64mime import body_decode
from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_mail(body, counts):
    user = "you@gmail.com"
    password = "******"

    print("preparing email content...\n")
    message = MIMEMultipart()
    message['Subject'] = "Today's Craigslist Car Listings (Newest " + str(counts) + ")"
    message['From'] = user
    message['To'] = user

    body_content = body
    message.attach(MIMEText(body_content, "html"))
    msg_body = message.as_string()

    server = SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(user, password)
    server.sendmail(user, user, msg_body)
    server.quit()