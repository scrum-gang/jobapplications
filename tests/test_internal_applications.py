import pytest
import os
import sys
from datetime import datetime

sys.path.insert(0, os.getcwd())
from utils import db
from tables import Application, Inhouse
from internal import get_applications_internal, apply_internal, update_status_internal

user_id = 1
job_id = 0
resume = "/potato/resume.pdf"



def test__apply_with_missing_info(test_teardown):
    """
    Failure scenario: Missing information should throw errors.
    """
    resume = ""
    with pytest.raises(Exception) as e:
        apply_internal(user_id, job_id, resume)


def test__update_status_empty_string(test_teardown):
    """
    Failure scenario: Empty status should give an error
    """
    user_id = 1

    # We create an application in the DB
    applications = apply_internal(user_id, job_id, resume)

    # We update the status of this application
    new_status = ""
    with pytest.raises(Exception) as e:
        update_status_internal(applications[0]['id'], new_status)


def test__apply(test_teardown):
    """
    Verifies that it is possible to apply to a job.

    This test also verifies querying applications by Job & User ID.
    """
    no_applications = get_applications_internal(job_id, 'job')
    assert len(no_applications) == 0

    resume = "/resumes/resume.pdf"
    apply_internal(user_id, job_id, resume)

    new_job_id = 5
    assert new_job_id != job_id
    apply_internal(user_id, new_job_id, resume)

    applications_by_job = get_applications_internal(new_job_id, 'job')
    applications_by_user = get_applications_internal(user_id, 'user')

    print(applications_by_user)
    assert len(applications_by_user) == 2
    assert len(applications_by_job) == 1
    assert applications_by_user[0]['is_inhouse_posting'] and applications_by_job[0]['is_inhouse_posting']
    assert applications_by_user[0]['resume'] == applications_by_job[0]['resume'] == resume
    assert applications_by_user[0]['job_id'] == job_id
    assert applications_by_user[0]['job_id'] != applications_by_job[0]['job_id']
    assert applications_by_user[0]['user_id'] == applications_by_job[0]['user_id'] == user_id
    assert applications_by_user[0]['application_id'] >= 0


def test__update_status(test_teardown):
    """
    Basic test for resetting the status
    """
    user_id = 1
    new_status = "new!"

    # We create an application in the DB
    applications = apply_internal(user_id, job_id, resume)
    updated_applications = update_status_internal(applications[0]['id'], new_status)

    assert applications[0]['status'] != new_status
    assert updated_applications[0]['status'] == new_status
    assert updated_applications[0]['id'] == applications[0]['id']
