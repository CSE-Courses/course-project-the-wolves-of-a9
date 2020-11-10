
# This file is a job to send the daily email to all users with a stored email

from scheduler.emailservice.email import Email
from scheduler.emailservice.news import build_report
import os
from django.contrib.auth.models import User

def sendDailyEmail():
    path = build_report()

    emails = []
    for eaddress in User.objects.all():
        if not eaddress.email == "":
            emails.append(eaddress.email)

    msg = Email(emails, "Wolves News", "Attached is your daily financial news report", [path])
    msg.send()
    os.remove(path)
    return
