import smtplib
from os.path import basename
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart

from confidential import personal_email, personal_password

#param: recipients: a list of email addresses as strings
#param: subject: a string to be the subject of the email
#param: message: a sting to be the message of the email
#param: attachments: optional list of file paths to be added as attachments
#function: send: the email will be sent as formatted by the params
class Email():
    def __init__(self, recipients, subject, message, attachments=[]):
        self.recipients = recipients
        self.subject = subject
        self.message = message
        self.attachments = attachments
        self.password = personal_password
        self.sender = personal_email

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
