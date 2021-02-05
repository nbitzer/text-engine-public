import argparse
import logging
import db

# Set up logging
logging.basicConfig(filename='/home/ubuntu/flaskapp/text-engine.log', filemode='a', format="%(asctime)s - %(levelname)s - %(name)s - %(message)s")
log = logging.getLogger("add_person.py")
log.setLevel(logging.INFO)

parser = argparse.ArgumentParser()
parser.add_argument('phone_number', type=str)
args = parser.parse_args()

try:
    db.add_person(args.phone_number, db.get_session())
except Exception as ex:
    log.error("{} is already in the system! Got error: {}".format(args.phone_number, ex))
