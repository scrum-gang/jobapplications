"""
Contains functionalities to apply to internal job postings.
"""
from datetime import datetime
from utils import db
import json

from tables import Application, Inhouse


def apply_internal(user_id, job_id, resume):
    """
    Basic logic for applying to internal job postings.

    Arguments:
    `user_id`: ID of the user applying
    `job_id`: ID of the job a user is applying for
    `resume`: Handy tool for applying to jobs
    """
    if not resume or job_id < 0 or user_id < 0:
        raise Exception("Please enter a resume name and a valid job & user id.")

    # TODO [aungur]: Refactor this double call to `db.session.commit`
    generic_application = Application(date=str(datetime.now()), user_id=user_id, is_inhouse_posting=True,
                                      status="Applied", resume=resume)
    db.session.add(generic_application)
    db.session.commit()

    inhouse_application = Inhouse(application_id=generic_application.id, job_id=job_id)
    db.session.add(inhouse_application)
    db.session.commit()

    user_applications = Application.query.filter_by(user_id=user_id).all()
    return json.dumps([application.to_dict() for application in user_applications])


def update_status_internal(application_id, new_status):
    """
    Simply update the status of an inhouse job posting

    Arguments:
    `application_id`: ID of the application whose status we're changing
    `new_status`: New status for this application
    """
    if not new_status or application_id < 0:
        raise Exception("Please give a valid new status and application ID.")
    application = Application.query.filter_by(id=application_id).first()
    application.status = new_status

    user_applications = Application.query.filter_by(user_id=application.user_id).all()
    return json.dumps([application.to_dict() for application in user_applications])


def get_applications_internal(identifier, type_of_id):
    """
    Basic function to get all internal applications for a given job or user ID.

    Arguments:
    `identifier`: ID of the job or user whose applications we wish to view
    `type_of_id`: Whether it's a JOB or USER ID.
    """
    if type_of_id == "user":
        applications = db.session.query(Application, Inhouse) \
                                 .filter(Application.user_id == identifier) \
                                 .filter(Inhouse.application_id == Application.id) \
                                 .all()
    elif type_of_id == "job":
        applications = db.session.query(Application, Inhouse) \
                                 .filter(Inhouse.job_id == identifier) \
                                 .filter(Inhouse.application_id == Application.id) \
                                 .all()
    else:
        raise Exception("You must give either a USER or JOB ID.")

    #TODO [aungur]: refactor this
    output = [{key: application.to_dict()[key] if key in application.to_dict() else inhouse.to_dict()[key] for key in application.to_dict().keys() ^ inhouse.to_dict().keys()}
              for application, inhouse in applications]

    return json.dumps(output)
