
# This file is used to run async jobs

from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from scheduler.jobs.mail import sendDailyEmail

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(sendDailyEmail, 'cron', day_of_week="0-4", hour="9", minute=0)
    scheduler.start()
