
# TiffTock
This application does the following:
- Exposes an API to create, get and delete reminders.
- Reminders are saved in a SQLite datebase
- Runs a scheduler that executes the reminder processes (email, sms, api call, *custom*)

## Uses & Use Cases
If you're a developer, hobbyist or a tinkerer and you need a simple way to make stuff happen automatically at specific times, this tool is pretty much what you need. Think of it as a DIY version of AWS Lambda but way easier to get into. In this codebase, a "Reminder Process" is the term I use that is analogous to a "Lambda" function.

Originally, I just wanted something to help my girlfriend remember stuff. She always asks me, "hey, can you remind me to do X?" To which I always respond, "Why don't you use Siri?" I could use Siri myself and then just pass the message along, or I could spend all day writing a program to do it for me! Efficiency! Anyway, that's why this codebase is around the context of reminders. That said, the custom code you can write doesn't have to be a reminder, it can essentially be anything you want that runs at a predetermined time that you can schedule with an API call.

To create a block of code to run at a scheduled time, simply write a class that inherits the RemindProcess abstract class and write your custom code inside of the "remind" function.

## Overview
This application has two parts. The API and the scheduler. 

### API
The API is written using Flask and has API endpoints that can:
- Add a reminder
- Get a reminder
- Get all reminders
- Delete a reminder.

### Scheduler
The scheduler periodically checks the SQLite database for tasks to run and adds them to the scheduler to execute asynchronously. It will automatically delete tasks that are in the past.

## Limitations
I wrote this to solve my own problem, so I didn't think about sending reminders to different people/computers. For instance, if you set up an email reminder, it sends all reminders using the same method to the same email address every time. This means you can't choose different recipients for each reminder.

## YEAH YEAH YEAH, JUST TELL ME HOW TO RUN IT
### Flask API

**Create .env file**
Open the `.sampleenv` file in the app directory and use it to create a file in the same directory called `.env`

This file is where you will keep all of your secrets and app settings.

At minimum, you need to specify API_KEY and API_URL.

If you will be running this application over the internet or open network, I recommend generating a cryptographically secure API key using the Python secrets library, like so:
```
import secrets
print(secrets.token_hex(32))
```

**Create your python virtual environment**
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
**Set FLASK_APP**
```
export FLASK_APP=app
```

**Create the SQLite database**
```
flask shell
from app.database import db
db.create_all()
exit()
```

**Run**
```
flask run
```

### Scheduler
Assuming the python virtual environment is running:
```
python3 scheduler.py
```

## Write your own scheduled code.
1. Change `database.py` to include another enum type for your new task type. You will have to recreate the database if you do this.
2. Change the `create_reminder()` function in `__init__.py` to validate your new type.
3. Write your custom code in `reminder.py` by creating a class that inherits from the `RemindProcess` abstract class. Put your custom code in the `remind` function.
4. Add a new remind process to the `registered_remind_processes` dictionary in `reminder_factory.py`