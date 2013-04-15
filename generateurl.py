
import sqlalchemy
from sys import argv
from models import Participant


def generateUrls(workerid):
    try:
        participant = Participant.query.filter(Participant.workerid == workerid).one()
        part = dict(assignmentid = participant.assignmentid,
                    workerid  = participant.workerid,
                    hitid   = participant.hitid)

    except sqlalchemy.orm.exc.NoResultFound:
        # If worker id isn't in the 
        part = dict(assignmentid = workerid,
                    workerid  = workerid,
                    hitid   = workerid)

    return ["http://frylock.psych.nyu.edu/exp/exp?assignmentId=%s&workerId=%s&hitId=%s" % (part['assignmentid'], part['workerid'], part['hitid']),
            "http://frylock.psych.nyu.edu:8000/mturk?assignmentId=%s&workerId=%s&hitId=%s" % (part['assignmentid'], part['workerid'], part['hitid']),
            "http://frylock.psych.nyu.edu:8000/exp?assignmentId=%s&workerId=%s&hitId=%s" % (part['assignmentid'], part['workerid'], part['hitid'])]

if __name__=="__main__":
    try:
        workerid = argv[1]
    except IndexError:
        print "USAGE: python generateurl.py assignmentid"
        print "If assignmentid is not in the database, url will include it in all fields (e.g., debug)"
        exit(0)
    urls = generateUrls(workerid)
    print "URLs for worker %s" % workerid
    for url in urls:
        print url
