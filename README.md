# Text-Engine
This app was built around the idea of sending text messages along with a journalism story. The texts would help immerse the reader in the story and add another aspect to how stories are told.

# Why?
The intent of this project was to build an application that would send time-based MMS messages to a user, leveraging Twilio.

# Stack
* Python is being used for all the logic
* [sqlite3](https://sqlite.org/) is being used as the datastore
  * The number from which received the original text
  * The time at which we sent the last text
  * Where we are in the string of texts to be sent (i.e. we've sent 15 out of 25 texts)
* [Flask](http://flask.pocoo.org/) is being used as the web server to receive POST requests from Twilio
* [Twilio](https://www.twilio.com/) us being used as the SMS/MMS service
* All of this is running on an [EC2 instance in AWS](https://aws.amazon.com/ec2/)
* [Bash](https://www.gnu.org/software/bash/) is being used to handle the starting/restarting of the python daemon (daemon.py)

# How it works
1. When a person texts the Twilio number, Twilio sends a POST request to whatever endpoint that's been configured in Twilio. In this case, it hits a Flask app running in EC2.
2. Once the POST request comes into the Flask app, I write the necesarry information to the sqlite3 dataebase. I write the following information:
    1. Number from which we received the text
    2. The time at which the number texted
    3. I assign a random story to be texted (just using an integer in the db that corresponds to an index in the story array)
    4. Lastly I instantiate the `next_text_number` to zero. This is an incrementing integer that's going to keep track of which text in which story we need to send next.
3. Once I have the information for the texter (ya, I said it) in the database, the daemon that's constantly running checks the database every second to see if someone needs to be texted.
4. If the daemon finds someone who needs to be texted (based of time deltas), we then make a request to the Twilio API with the necessary information and Twilio handles the rest :)
