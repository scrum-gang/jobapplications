"""
Contains functionalities relevant to job applications regardless
of their type.
"""
from datetime import datetime
from utils import db

from tables import Application, External, Inhouse

def get_application_by_id(application_id):
    """
    Fetches all applications based on an application ID.

    TODO [aungur]: This should probably be refactored ...
    """
    application = Application.query.filter_by(id=application_id).first()
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
