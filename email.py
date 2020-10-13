import smtplib
from os.path import basename
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart


class Email():
    def __init__(self, recipients, subject, message, attachments=[]):
        self.recipients = recipients
        self.subject = subject
        self.message = message
        self.attachments = attachments
        self.password = "placeholder"
        self.sender = 'eric.santulli@gmail.com'

    def send(self):
        msg = MIMEMultipart()
        msg['From'] = self.sender
        msg['To'] = ", ".join(self.recipients)
        msg['Subject'] = self.subject
        msg.attach(MIMEText(self.message, 'plain'))

        for path in self.attachments:
            with open(path, "rb") as reader:
                attachment = MIMEApplication(reader.read())
            attachment.add_header('Content-Disposition', 'attachment', filename=basename(path))
            msg.attach(attachment)

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(self.sender, self.password)
        server.sendmail(self.sender, self.recipients, msg.as_string())
        server.quit()
