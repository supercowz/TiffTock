from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Reminder(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  when = db.Column(db.DateTime, nullable=False)
  message = db.Column(db.String(120), nullable=False)
  method = db.Column(db.Enum('email', 'sms', 'api', name='reminder_method'), nullable=False, default='email')