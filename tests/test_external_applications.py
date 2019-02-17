import pytest
import json
import os
import sys
import time

sys.path.insert(0, os.getcwd())
from external import apply_external_posting, update_status_external_posting, get_applications_external


def test__apply_with_missing_info(test_teardown):
    """
    Failure scenario: Missing information should throw errors.
    """
    user_id = 0
    job_url, job_title, job_season = "", "", ""

    with pytest.raises(Exception) as e:
        apply_external_posting(user_id, job_url, job_title, job_season)


def test__apply_with_existing_season(test_teardown):
    """
    Success scenario: It shouldn't matter if the season already exists or not.
    """
    user_id = 1
    job_url, job_title, job_season = "url.com", "potato", "winter"
    
    # We create an application in the DB
    apply_external_posting(user_id, job_url, job_title, job_season)

    # We create another application in the same job season
    applications = json.loads(apply_external_posting(user_id, job_url, job_title, job_season))

    assert len(applications) == 2
    assert applications[0]['season'] == applications[1]['season']
    assert applications[0]['status'] == applications[1]['status'] == "applied"


def test__update_status_empty_string(test_teardown):
    """
    Failure scenario: Empty status should give an error
    """
    user_id = 1
    job_url, job_title, job_season = "url.com", "potato", "winter"

    # We create an application in the DB
    applications = json.loads(apply_external_posting(user_id, job_url, job_title, job_season))

    # We update the status of this application
    new_status = ""
    with pytest.raises(Exception) as e:
        update_status_external_posting(applications[0]['id'], new_status)


def test__apply(test_teardown):
    """
    Regular scenario for applying to external postings
    """
    user_id = 1
    job_url, job_title, job_season = "url.com", "potato", "winter"
    
    # We create an application in the DB
    apply_external_posting(user_id, job_url, job_title, job_season)
    applications = json.loads(get_applications_external(user_id))

    assert applications[0]['user_id'] == user_id
    assert applications[0]['is_inhouse_posting'] == False
    assert applications[0]['job_url'] == job_url
    assert applications[0]['job_title'] == job_title
    assert applications[0]['season'] == job_season


def test__update_status(test_teardown):
    """
    Regular scenario for updating a status
    """
    user_id = 1
    job_url, job_title, job_season = "url.com", "potato", "winter"
    new_status = "new!"

    # We create an application in the DB
    applications = json.loads(apply_external_posting(user_id, job_url, job_title, job_season))
    updated_applications = json.loads(update_status_external_posting(applications[0]['id'], new_status))

    assert applications[0]['status'] != new_status
    assert updated_applications[0]['status'] == new_status
    assert updated_applications[0]['id'] == applications[0]['id']
