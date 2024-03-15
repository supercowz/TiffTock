import os
from datetime import datetime
from dotenv import load_dotenv
from flask import Flask, request, jsonify

from app.database import db, Reminder

def create_app(test_config=None):
  
  app = Flask(__name__)
  app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

  db.init_app(app)

  with app.app_context():
    db.create_all()

  ## Setup environment variables from .env
  load_dotenv()
  API_KEY = os.getenv('API_KEY')

  # This web api is intended to be used by a single user, so we can use a single API key
  # You can generate an API key using the following code
  # import secrets
  # print(secrets.token_hex(32))

  # Auth guard
  @app.before_request
  def check_api_key():
    if request.headers.get('x-api-key') != API_KEY:
      return jsonify({'error': 'invalid api key'}), 401

  @app.route('/remind', methods=['POST'])
  def create_reminder():
    data = request.json
    if 'when' not in data or 'message' not in data:
      return jsonify({'error': 'invalid input'}), 400
    
    try:
      data['when'] = datetime.fromisoformat(data['when'])
    except ValueError:
      return jsonify({'error': 'invalid datetime'}), 400

    if data.get('method') not in ['email', 'sms', 'api']:
      return jsonify({'error': 'invalid method'}), 400

    reminder = Reminder(when=data['when'], message=data['message'], method=data.get('method'))
    db.session.add(reminder)
    db.session.commit()

    return jsonify({'id': reminder.id}), 201

  @app.route('/reminder/<int:reminder_id>', methods=['GET'])
  def get_reminder(reminder_id):
    reminder = Reminder.query.get(reminder_id)
    if reminder is None:
      return jsonify({'error': 'reminder not found'}), 404
    
    #jsonify the object
    
    return jsonify({'id': reminder.id, 'when': datetime.isoformat(reminder.when), 'message': reminder.message, 'method': reminder.method})

  @app.route('/reminder/<int:reminder_id>', methods=['DELETE'])
  def delete_reminder(reminder_id):
    reminder = Reminder.query.get(reminder_id)
    if reminder is None:
      return jsonify({'error': 'reminder not found'}), 404
    
    db.session.delete(reminder)
    db.session.commit()
    return '', 204

  @app.route('/reminders', methods=['GET'])
  def get_reminders():
    reminders = Reminder.query.all()
    json_reminders = map(lambda r: {'id': r.id, 'when': datetime.isoformat(r.when), 'message': r.message, 'method': r.method}, reminders)
    return jsonify(list(json_reminders))

  return app