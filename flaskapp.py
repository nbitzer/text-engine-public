"""
Super basic Flask app being used to handle POST requests from Twilio.
"""
import db
import logging
from flask import Flask, request, redirect
from twilio import twiml
app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True

# Set up logging
logging.basicConfig(filename='/home/ubuntu/flaskapp/text-engine.log', filemode='a', format="%(asctime)s - %(levelname)s - %(name)s - %(message)s")
log = logging.getLogger("flaskapp.py")
log.setLevel(logging.INFO)

@app.route('/')
def home():
    """
    End point we can hit just to make sure the Flask app is stood up.
    :returns: String
    """
    return "Server is running..."

@app.route('/sms', methods=['GET', 'POST'])
def sms():
    """
    When this endpoint is hit we call out db class and write the necessary information to out DB.
    :returns: Must return a Twiml response.
    """
    number = request.form['From']
    log.info("Received text from: {}".format(number))
    try:
        db.add_person(number, db.get_session())
    except Exception as ex:
        log.info("ERROR FROM FLASK APP: {}".format(ex))
    return str(twiml.Response())

if __name__ == '__main__':
  app.run()
