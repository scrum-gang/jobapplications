"""
Contains functionalities relevant to job applications regardless
of their type.
"""
from datetime import datetime
from utils import db

from tables import Application, External, Inhouse

def get_application_by_id(application_id, user_id):
    """
    Fetches all applications based on an application ID.

    TODO [aungur]: This should probably be refactored ...
    """
    application = Application.query.filter_by(id=application_id, user_id=user_id).first()
    if not application:
        return {"status": "Application not found!"}
    if application.is_inhouse_posting:
        app_data, type_data = db.session.query(Application, Inhouse) \
                                .filter(Application.id == application_id) \
                                .filter(Inhouse.application_id == Application.id) \
                                .first()
    else:
        app_data, type_data = db.session.query(Application, External) \
                                .filter(Application.id == application_id) \
                                .filter(External.application_id == Application.id) \
                                .first()
    full_application_data = {key: app_data.to_dict()[key] if key in app_data.to_dict() else type_data.to_dict()[key] for key in app_data.to_dict().keys() ^ type_data.to_dict().keys()}
    return full_application_data


def update_comment(application_id, new_comment, user_id):
    """
    Updates a comment to an application
    """
    if not application_id or not new_comment:
        return {"status": "Please provide an application ID and a new comment!"}
    if not user_id:
        return {"status": "Please make sure you are authenticated."}

    application = Application.query.filter_by(id=application_id, user_id=user_id).first()
    if not application:
        return {"status": "Application not found!"}
    
    application.comment = new_comment
    user_applications = Application.query.filter_by(user_id=application.user_id).all()
    return [application.to_dict() for application in user_applications]


def update_status(application_id, new_status, user_id):
    """
    Updates the status of a user for a given job application

    Arguments:
    application_id: ID of the application
    new_status: New status of the user for that application
    """
    if not new_status:
        return {"status": "You must provide a non-empty new status."}

    application = Application.query.filter_by(id=application_id, user_id=user_id).first()
    application.status = new_status
    user_applications = Application.query.filter_by(user_id=application.user_id).all()
    return [application.to_dict() for application in user_applications]


def withdraw_application(application_id, user_id):
    """
    Deletes a user's application.
    """
    if not application_id:
        return {"status": "No application ID provided."}

    application = Application.query.filter_by(id=application_id, user_id=user_id).first()

    if application.is_inhouse_posting:
        specific_application = Inhouse.query.filter_by(application_id=application_id).first()
    else:
        specific_application = External.query.filter_by(application_id=application_id).first()

    if not application:
        return {"status": "No application found."}

    db.session.delete(specific_application)
    db.session.delete(application)
    db.session.commit()
    return {"status": "success"}
