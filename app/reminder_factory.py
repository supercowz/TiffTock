from reminder import EmailRemindProcess, SMSRemindProcess, APIRemindProcess

registered_remind_processes = {
  'email': EmailRemindProcess,
  'sms': SMSRemindProcess,
  'api': APIRemindProcess
}

class RemindProcessFactory:
  @staticmethod
  def create(reminder):
    rp = reminder.get('method')
    if rp in registered_remind_processes:
      return registered_remind_processes[rp](reminder)
    
    else:
      raise ValueError('Invalid reminder method')