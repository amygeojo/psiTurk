
import csv
import sys

from db import db_session
from models import Participant

def mark_completed(assignmentId):
    try:
        user = Participant.query.\
                filter(Participant.assignmentid == assignmentId).\
                one()
        user.status = 5
        db_session.add(user)
        db_session.commit()
        print "Marked as credited", assignmentId
    except:
        print "could not find", assignmentId


if __name__ == '__main__':
    fn = sys.argv[1]
    with open(fn, 'rb') as csvfile:
        submissionreader = csv.reader(csvfile)
        for row in submissionreader:
            mark_completed(row[3])

