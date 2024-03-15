import os
import requests
from abc import ABC, abstractmethod

class RemindProcess(ABC):
  @abstractmethod
  def __init__(self, reminder):
    if reminder.get('id') is None:
      raise ValueError('id is required')
    if reminder.get('when') is None:
      raise ValueError('when is required')
    if reminder.get('message') is None:
      raise ValueError('message is required')
    
    self.id = reminder['id']
    self.when = reminder['when']
    self.message = reminder['message']

  '''
  Do the reminder action. For example, send an email.'''
  @abstractmethod
  def remind(self, message: str):
    pass

class EmailRemindProcess(RemindProcess):
  def __init__(self, reminder):
    self.__setup_mailgun()
    super().__init__(reminder)

  def __setup_mailgun(self):
    if os.environ.get('MAILGUN_API_KEY') is None:
      raise ValueError('MAILGUN_API_KEY is required')
    if os.environ.get('MAILGUN_EMAIL_FROM') is None:
      raise ValueError('MAILGUN_EMAIL_FROM is required')
    if os.environ.get('MAILGUN_EMAIL_TO') is None:
      raise ValueError('MAILGUN_EMAIL_TO is required')
    if os.environ.get('MAILGUN_EMAIL_DOMAIN') is None:
      raise ValueError('MAILGUN_EMAIL_DOMAIN is required')
    
    self.mailgun_api_key = os.environ['MAILGUN_API_KEY']
    self.mailgun_email_from = os.environ['MAILGUN_EMAIL_FROM']
    self.mailgun_email_to = os.environ['MAILGUN_EMAIL_TO']
    self.mailgun_email_domain = os.environ['MAILGUN_EMAIL_DOMAIN']

  def remind(self, message: str):
    response = requests.post(
    f"https://api.mailgun.net/v3/{self.mailgun_email_domain}/messages",
    auth=("api", self.mailgun_api_key), 
    data={
      f"from": f"Chris Bednar <{self.mailgun_email_from}>",
      "to": [f"{self.mailgun_email_to}"],
      "subject": "This is a test message from mailgun",
      "text": message
    })

    return response

from twilio.rest import Client
class SMSRemindProcess(RemindProcess):
  def __init__(self, reminder):
    self.__setup_twilio()
    super().__init__(reminder)

  def __setup_twilio(self):
    if os.environ.get('TWILIO_ACCOUNT_SID') is None:
      raise ValueError('TWILIO_ACCOUNT_SID is required')
    if os.environ.get('TWILIO_AUTH_TOKEN') is None:
      raise ValueError('TWILIO_AUTH_TOKEN is required')
    if os.environ.get('TWILIO_PHONE_NUMBER_FROM') is None:
      raise ValueError('TWILIO_PHONE_NUMBER_FROM is required')
    if os.environ.get('TWILIO_PHONE_NUMBER_TO') is None:
      raise ValueError('TWILIO_PHONE_NUMBER_TO is required')
    
    self.twilio_account_sid = os.environ['TWILIO_ACCOUNT_SID']
    self.twilio_auth_token = os.environ['TWILIO_AUTH_TOKEN']
    self.twilio_phone_number_from = os.environ['TWILIO_PHONE_NUMBER_FROM']
    self.twilio_phone_number_to = os.environ['TWILIO_PHONE_NUMBER_TO']

  def remind(self, message: str):
    twilio_client = Client(self.twilio_account_sid, self.twilio_auth_token)

    message = twilio_client.messages \
      .create(
        body=message,
        from_=self.twilio_phone_number_from,
        to=self.twilio_phone_number_to
      )
    
    return message
    
class APIRemindProcess(RemindProcess):
  def __init__(self, reminder):
    self.__setup_api()
    super().__init__(reminder)

  def __setup_api(self):
    if os.environ.get('API_REMIND_URL') is None:
      raise ValueError('API_REMIND_URL is required')
    
    self.api_remind_url = os.environ['API_REMIND_URL']
  
  # In the future, we can add more functionality to this method. 
  # For now, the API endpoint is hardcoded, assumed to be a POST and the message is the only parameter
  def remind(self, message: str):
    response = requests.post(
      self.api_remind_url,
      json={
        'message': message
      }
    )

    return response