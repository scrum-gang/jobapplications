"""
Contains functionalities to apply to external job applications.
"""
from datetime import datetime
from utils import db

from tables import Application, External


def apply_external(user_id, url, position, company, resume, date_posted, deadline, status="Applied"):
    """
    Applies to an external job posting

    Arguments:
    user_id: User applying for the job
    url: URL for the job they are applying to
    position: Position of the job they are applying to
    company: Company they are applying to
    date_posted: When the job posting was created
    deadline: Deadline for the job
    """
    if not url or not position or not company:
        raise Exception("You must provide a job URL, position and company.")
    for application in Application.query.filter_by(user_id=user_id).all():
        external = External.query.filter_by(company=company, position=position, application_id=application.id).first()
        if external:
            return [{"status": f"Already found an application to {position} at {company} for {user_id}!"}]

    application = Application(date=str(datetime.now()), user_id=user_id,
                              is_inhouse_posting=False, status=status, resume=resume)
    db.session.add(application)
    db.session.commit()

    external_application = External(application_id=application.id, url=url, position=position,
                                    company=company, date_posted=date_posted, deadline=deadline)
    db.session.add(external_application)
    db.session.commit()
    user_applications = Application.query.filter_by(user_id=user_id).all()

    return [application.to_dict() for application in user_applications]


def update_status_external(application_id, new_status):
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
    return [application.to_dict() for application in user_applications]


def get_applications_external(user_id):
    """
    Simply returns all external postings associated to a user
    """
    applications = db.session.query(Application, External) \
                             .filter(Application.user_id == user_id) \
                             .filter(External.application_id == Application.id) \
                             .all()
    #TODO [aungur]: refactor this
    output = [{key: application.to_dict()[key] if key in application.to_dict() else external.to_dict()[key] for key in application.to_dict().keys() ^ external.to_dict().keys()}
              for application, external in applications]

    return output
