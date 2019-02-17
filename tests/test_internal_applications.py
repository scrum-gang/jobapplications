import pytest
import json
import os
import sys
from datetime import datetime

sys.path.insert(0, os.getcwd())
from utils import db
from tables import Application, Inhouse, Season
from internal import get_applications_internal

job_id = 0


def test_get_applications_internal(test_teardown):
    """
    Verifies that it is possible to get internal applications
    by job ID. The calls made directly to the database may be
    replaced by calls to the functions for creating inhouse
    applications.
    """
    no_applications = json.loads(get_applications_internal(job_id))
    assert len(no_applications) == 0

    resume, comments = "/resumes/resume.pdf", "test"
    creation_date_inhouse = str(datetime.now())
    user_id, season_name, status = 1, "Fall", "applied"
    season = Season(name=season_name)
    generic_application = Application(date=creation_date_inhouse, user_id=user_id, season=season_name,
                                      is_inhouse_posting=True, status=status)
    inhouse_application = Inhouse(application_id=generic_application.id, job_id=job_id,
                                  resume=resume, comments=comments)
    db.session.add(season)
    db.session.add(generic_application)
    db.session.add(inhouse_application)
    db.session.commit()

    applications = json.loads(get_applications_internal(job_id))
    assert len(applications) == 1
    assert applications[0]['is_inhouse_posting']
    assert applications[0]['resume'] == resume and applications[0]['season'] == season_name
    assert applications[0]['date'] == creation_date_inhouse
    assert applications[0]['job_id'] == job_id and applications[0]['user_id'] == user_id
