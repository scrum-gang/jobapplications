from datetime import datetime
import pytest
import os
import sys
import time
sys.path.insert(0, os.getcwd())

from utils import db
from tables import Application, Inhouse, External

# Global Variables
user_id = 0
status = "Applied"
resume = "/this/resume/"


def test_db_is_created():
    """
    Ensures that the database is created and contains
    the correct tables.

    If the tables exist, we can query them with no exceptions thrown.
    """
    try:
        applications = Application.query.first()
        inhouse_postings = Inhouse.query.first()
        external_postings = External.query.first()
    except Exception:
        assert False
    assert True


def test_db_can_add_applications():
    """
    Creates two generic applications in the database.
    Later tests specify that one is an inhouse application while the other is an
    external one.
    """
    creation_date_inhouse = datetime.now()
    time.sleep(1)
    creation_date_external = datetime.now()

    inhouse_application = Application(date=creation_date_inhouse, user_id=user_id, is_inhouse_posting=True,
                                      status=status, resume=resume)
    external_application = Application(date=creation_date_external, user_id=user_id, is_inhouse_posting=False,
                                       status=status, resume=resume)
    db.session.add(inhouse_application)
    db.session.add(external_application)

    applications_from_db = Application.query.filter_by(user_id=user_id,status=status).all()
    for application in applications_from_db:
        assert application is not None
        assert application.status is "Applied"
        if application.is_inhouse_posting:
            assert application.date == creation_date_inhouse
        else:
            assert application.date == creation_date_external


def test_db_can_add_inhouse_application():
    """
    Ensures that it is possible to add an inhouse application.
    This relies on a previous test creating the generic `Application` associated to
    the inhouse application
    """
    job_application = Application.query.filter_by(user_id=user_id, status=status, is_inhouse_posting=True,
                                                  resume=resume).first()
    job_id = 0
    inhouse_application = Inhouse(application_id=job_application.id, job_id=job_id)
    db.session.add(inhouse_application)

    inhouse_application_from_db = Inhouse.query.filter_by(application_id=job_application.id).first()
    assert inhouse_application_from_db is not None
    assert job_application.resume is resume
    assert inhouse_application_from_db.job_id is job_id


def test_db_can_add_external_application():
    """
    Ensures that it is possible to add an external application
    This relies on a previous test creating the generic `Application` associated
    to the external application
    """
    job_application = Application.query.filter_by(user_id=user_id, status=status,
                                                  is_inhouse_posting=False, resume=resume).first()
    url = "linkedin.com/job"
    position, company = "potato master", "potato land"
    date_posted, deadline = str(datetime.now()), str(datetime.now())

    external_application = External(application_id=job_application.id, url=url, position=position,
                                    company=company, date_posted=date_posted, deadline=deadline)
    db.session.add(external_application)

    external_application_from_db = External.query.filter_by(application_id=job_application.id).first()
    assert external_application_from_db is not None
    assert external_application_from_db.url is url
    assert external_application_from_db.company is company
    assert external_application_from_db.date_posted is date_posted
    assert external_application_from_db.deadline is deadline
