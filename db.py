"""
Class to handle all sqlite database actions.
"""


import datetime
import logging
import sqlalchemy
import sqlalchemy.ext.declarative
import sqlalchemy.orm
from random import randint
from text_sequence import get_text_sequence

# Set up logging
logging.basicConfig(filename='/home/ubuntu/flaskapp/text-engine.log', filemode='a', format="%(asctime)s - %(levelname)s - %(name)s - %(message)s")
log = logging.getLogger("db.py")
log.setLevel(logging.INFO)

_SQLALCHEMY_BASE = sqlalchemy.ext.declarative.declarative_base()

class Person(_SQLALCHEMY_BASE):
    __tablename__ = 'person'
    phone_number = sqlalchemy.Column(sqlalchemy.String(20), primary_key=True)
    text_story_index = sqlalchemy.Column(sqlalchemy.Integer)
    next_text_number = sqlalchemy.Column(sqlalchemy.Integer)
    next_text_time = sqlalchemy.Column(sqlalchemy.DateTime)

# Setup database.
_DATABASE = sqlalchemy.create_engine('sqlite:////home/ubuntu/flaskapp/text.db')
_SQLALCHEMY_BASE.metadata.create_all(_DATABASE)
_DATABASE_SESSION = sqlalchemy.orm.sessionmaker(bind=_DATABASE)

def get_session():
    """
    Get database session.
    :returns: database session object
    """
    return _DATABASE_SESSION()

def add_person(phone_number, session):
    """
    When a person text the Twilio number, they will be added to the database with the necessary information.
    :param phone_number: Phone number of the person who texted the Twilio number.
                         This is the number we'll use to text the stories back to.
    :param session: Session for the databse connection.
    :return: None
    """
    # I tried to simplify the getting of the length for the array, but python kept complaining.
    text_stories_length = len(get_text_sequence())
    text_stories_length -= 1
    text_story = randint(0,int(text_stories_length))
    first_text_time = datetime.datetime.now() + get_text_sequence()[text_story][0][1]
    log.info("Text time for phone {} is: {}".format(phone_number, first_text_time))
    person = Person(phone_number=phone_number,
                    text_story_index = text_story, # Randmonly choosen story we're going to text.
                    next_text_number = 0,
                    next_text_time = first_text_time)
    session.add(person)
    session.commit()
    log.info("Added number: {} to database. Getting story: {} ".format(phone_number, text_story))

def next_person(session):
    """
    Get the next person(s) you should text
    :param session: Database session object
    """
    return session.query(Person).order_by(Person.next_text_time).first()

def prepare_for_next_text(person, session):
    """
    Figures out which text needs to be send to what phone number. Also handles the deletion of
    phone numbers from the database once all the texts for a given story have been sent.
    :param person: Database object for a given phone number (aka person)
    :param session: Session for the database connection.
    """
    # If there are no more texts in the story, delete the person from the databse.
    if person.next_text_number + 1 >= len(get_text_sequence()[person.text_story_index]):
        log.info("Deleting {} from the database!".format(person.phone_number))
        session.delete(person)
        session.commit()
    # There are still texts to send
    else:
        log.info("Story index: {}, Current Text Number: {}".format(person.text_story_index, person.next_text_number))
        person.next_text_time = (
            datetime.datetime.now() +
            get_text_sequence()[person.text_story_index][person.next_text_number + 1][1])
        person.next_text_number = person.next_text_number + 1
        session.commit()
