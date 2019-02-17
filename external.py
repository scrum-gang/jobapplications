"""
Contains functionalities to apply to external job postings.
"""
from datetime import datetime
from utils import db
import json

from tables import Season, Application, External


def apply_external_posting(user_id, job_url, job_title, job_season):
    """
    Applies to an external job posting

    Arguments:
    user_id: User applying for the job
    job_url: URL for the job they are applying to
    job_title: Title of the job they are applying to
    job_season: Season during which the job takes place
    """
    if not job_url or not job_title or not job_season:
        raise Exception("You must provide a job URL, job title and job season.")

    season = Season.query.filter_by(name=job_season).first()
    if not season:
        season = Season(name=job_season)
        db.session.add(season)

    application = Application(date=str(datetime.now()), user_id=user_id,
                              is_inhouse_posting=False, season=season.name,
                              status="applied")
    db.session.add(application)

    external_application = External(application_id=application.id, job_url=job_url,
                                    job_title=job_title) 
    db.session.add(external_application)
    db.session.commit()
    user_applications = Application.query.filter_by(user_id=user_id).all()

    return json.dumps([application.to_dict() for application in user_applications])


def update_status_external_posting(application_id, new_status):
    """
    Updates the status of a user for a given job application

    Arguments:
    application_id: ID of the application
    new_status: New status of the user for that application
    """
    if not new_status:
        raise Exception("You must provide a non-empty status.")

    application = Application.query.filter_by(id=application_id).first()
    application.status = new_status
    user_applications = Application.query.filter_by(user_id=application.user_id).all()
    return json.dumps([application.to_dict() for application in user_applications])

def get_applications_external(user_id):
    """
    Simply returns all external postings associated to a user
    """
    applications = db.session.query(Application, External).filter(Application.user_id == user_id).all()
    #TODO [aungur]: refactor this
    output = [{key: application.to_dict()[key] if key in application.to_dict() else external.to_dict()[key] for key in application.to_dict().keys() ^ external.to_dict().keys()}
              for application, external in applications]

    return json.dumps(output)
