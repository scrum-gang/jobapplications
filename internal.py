"""
Contains functionalities to apply to internal job postings.
"""
from datetime import datetime
from utils import db
import json

from tables import Application, Inhouse


def get_applications_internal(job_id):
    """
    Basic function to get all internal applications for a given job ID.

    Arguments:
    job_id: ID of the job whose applications we wish to view
    """
    applications = db.session.query(Application, Inhouse).filter(Inhouse.job_id == job_id).all()
    #TODO [aungur]: refactor this
    output = [{key: application.to_dict()[key] if key in application.to_dict() else inhouse.to_dict()[key] for key in application.to_dict().keys() ^ inhouse.to_dict().keys()}
              for application, inhouse in applications]

    return json.dumps(output)
