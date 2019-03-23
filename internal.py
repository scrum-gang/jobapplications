"""
Contains functionalities to apply to internal job applications.
"""
from datetime import datetime
from utils import db

from tables import Application, Inhouse


def apply_internal(user_id, job_id, resume, comment):
    """
    Basic logic for applying to internal job postings.

    Arguments:
    `user_id`: ID of the user applying
    `job_id`: ID of the job a user is applying for
    `resume`: Handy tool for applying to jobs
    """
    if not user_id:
        return {"status": "Please double check your authentication token, no user ID found."}
    if not resume:
        return {"status": "Please enter a resume!"}
    if not job_id:
        return {"status": "Please make sure you are applying to a job with a non-null ID!"}
    for application in Application.query.filter_by(user_id=user_id):
        inhouse = Inhouse.query.filter_by(application_id=application.id, job_id=job_id).first()
        if inhouse:
            return {"status": f"Already found an application for this job for the user {user_id}"}
    generic_application = Application(date=str(datetime.now()), user_id=user_id, is_inhouse_posting=True,
                                      status="Applied", resume=resume, comment=comment)
    db.session.add(generic_application)
    db.session.commit()

    inhouse_application = Inhouse(application_id=generic_application.id, job_id=job_id)
    db.session.add(inhouse_application)
    db.session.commit()

    user_applications = Application.query.filter_by(user_id=user_id).all()
    return [application.to_dict() for application in user_applications]


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

    return output
