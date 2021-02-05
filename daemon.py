"""
This is the daemon that's going to be constantly running on the EC2 instance checking the database.
"""


import datetime
import logging
import os
import db
from text_sequence import get_text_sequence
from twilio.rest import TwilioRestClient
import time

# Set up logging
logging.basicConfig(filename='/home/ubuntu/flaskapp/text-engine.log', filemode='a', format="%(asctime)s - %(levelname)s - %(name)s - %(message)s")
log = logging.getLogger("daemon.py")
log.setLevel(logging.INFO)
log.info("Daemon started!")

# Twilio Account Info
# Using OS environment settings in order to keep secrets out of the source code
ACCOUNT_SID = str(os.environ["TWILIO_ACC"])
AUTH_TOKEN = str(os.environ["TWILIO_AUTHENTICATION"])
TWILIO_PHONE_NUMBER = str(os.environ["TWILIO_PHONE"])
log.info("Initiating daemon with Twilio credentials: {}, {}".format(ACCOUNT_SID, AUTH_TOKEN))
client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)

while True:
    session = db.get_session()
    next_text_person = db.next_person(session)
    if not next_text_person or \
       next_text_person.next_text_time > datetime.datetime.now():
        time.sleep(1)
        continue
    log.info("Sending text {} to {}".format(
        get_text_sequence()[next_text_person.text_story_index][next_text_person.next_text_number][0],
        next_text_person.phone_number))
    # Send test logic
    # If the text is a jpg, then use the Twilio media fuction
    if '.jpg' in get_text_sequence()[next_text_person.text_story_index][next_text_person.next_text_number][0]:
        message = client.messages.create(to=next_text_person.phone_number,
                                         from_=TWILIO_PHONE_NUMBER,
                                         media_url=get_text_sequence()[next_text_person.text_story_index][next_text_person.next_text_number][0])
    # Text isn't media, send normal text                                     
    else:
        message = client.messages.create(to=next_text_person.phone_number,
                                         from_=TWILIO_PHONE_NUMBER,
                                         body=get_text_sequence()[next_text_person.text_story_index][next_text_person.next_text_number][0])
    db.prepare_for_next_text(next_text_person, session)
