import os
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
  
  @abstractmethod
  def __init__(self, id, when, message):
    self.id = id
    self.when = when
    self.message = message

  '''
  Do the reminder action. For example, send an email.'''
  @abstractmethod
  def remind(self, message: str):
    pass

class EmailRemindProcess(RemindProcess):
  def __init__(self, reminder):
    super().__init__(reminder)
  
  def __init__(self, id, when, message):
    super().__init__(id, when, message)

  def remind(self, message: str):
    print(f"Sending email to {self.message} with message: {message}")

from twilio.rest import Client
class SMSRemindProcess(RemindProcess):
  def __init__(self, reminder):
    self.__setup_twilio()
    super().__init__(reminder)
  
  def __init__(self, id, when, message):
    self.__setup_twilio()
    super().__init__(id, when, message)

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
    
class APIRemindProcess(RemindProcess):
  def __init__(self, reminder):
    super().__init__(reminder)
  
  def __init__(self, id, when, message):
    super().__init__(id, when, message)

  def remind(self, message: str):
    print(f"Sending API request to {self.message} with message: {message}")

# def send_email(message):
#   return requests.post(
# 		"https://api.mailgun.net/v3/sandbox3801ca6e8cb7450cbe0dfe2a282021a5.mailgun.org/messages",
# 		auth=("api", MAILGUN_API_KEY), 
# 		data={
#       f"from": f"Chris Bednar <{MAILGUN_EMAIL_FROM}>",
# 			"to": [f"{MAILGUN_EMAIL_TO}"],
# 			"subject": "This is a test message from mailgun",
# 			"text": message
#     })

# def send_sms(message):
