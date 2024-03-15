import os
import requests
from datetime import datetime
from dotenv import load_dotenv
from apscheduler.schedulers.background import BackgroundScheduler

from reminder_factory import RemindProcessFactory

## Load environment variables
load_dotenv()
API_KEY = os.getenv('API_KEY')
API_URL = os.getenv('API_URL')
TWILIO_ACCOUNT_SID = os.environ['TWILIO_ACCOUNT_SID']
TWILIO_AUTH_TOKEN = os.environ['TWILIO_AUTH_TOKEN']
TWILIO_PHONE_NUMBER_TO = os.environ['TWILIO_PHONE_NUMBER_TO']
TWILIO_PHONE_NUMBER_FROM = os.environ['TWILIO_PHONE_NUMBER_FROM']
MAILGUN_API_KEY = os.environ['MAILGUN_API_KEY']
MAILGUN_EMAIL_TO = os.environ['MAILGUN_EMAIL_TO']
MAILGUN_EMAIL_FROM = os.environ['MAILGUN_EMAIL_FROM']

scheduler = BackgroundScheduler()

def start():
  # Check reminders every 10 seconds
  scheduler.add_job(
    check_reminders,
    'interval',
    seconds=10
  )

  # Clear reminders every 2 minutes
  scheduler.add_job(
    clear_reminders,
    'interval',
    minutes=2
  )

  scheduler.start()

def shutdown():
  scheduler.shutdown()

def check_reminders():
  reminders = get_reminders()

  for reminder in reminders:
    reminder_datetime = datetime.fromisoformat(reminder['when'])
    if scheduler.get_job(f"remind_{reminder['id']}") is None and reminder_datetime > datetime.now(): 
      print(f"adding job to scheduler: {reminder['id']}: {reminder['when']}")
      scheduler.add_job(
        jobstore='default',
        id=f"remind_{reminder['id']}",
        func=send_reminder,
        trigger='date',
        run_date=reminder_datetime,
        args=[reminder]
      )
    else:
      print(f"job not added to scheduler: {reminder['id']}: {reminder['when']}")

def get_reminders():
  reminders = requests.get(f'{API_URL}/reminders', headers={'x-api-key': API_KEY}).json()
  return reminders

def clear_reminders():
  reminders = get_reminders()
  for reminder in reminders:
    when = datetime.fromisoformat(reminder['when'])
    if when < datetime.now() and scheduler.get_job(f"remind_{reminder['id']}") is None:
      requests.delete(f'{API_URL}/reminder/{reminder["id"]}', headers={'x-api-key': API_KEY})  

def send_reminder(reminder):
  message = reminder['message']
  reminder = RemindProcessFactory.create(reminder)
  reminder.remind(message)

if __name__ == '__main__':
  start()
  try:
    while True:
      pass

  except (KeyboardInterrupt, SystemExit):
    shutdown()