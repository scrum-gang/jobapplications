from datetime import datetime
import pytest
import json
import os
import sys

sys.path.insert(0, os.getcwd())
from external import apply_external_posting, update_status_external_posting, get_applications_external

resume = "/potato/IamAPotato"
url, position, company = "url.com", "potato", "poutine factory"
date_posted, deadline = str(datetime.now()), str(datetime.now())


def test__apply_with_missing_info(test_teardown):
    """
    Failure scenario: Missing information should throw errors.
    """
    user_id = 0
    url, position, company = "", "", ""

    with pytest.raises(Exception) as e:
        apply_external_posting(user_id, url, position, company, resume, date_posted, deadline)


def test__apply_with_existing_season(test_teardown):
    """
    Success scenario: It shouldn't matter if the season already exists or not.
    """
    user_id = 1
    
    # We create an application in the DB
    apply_external_posting(user_id, url, position, company, resume, date_posted, deadline)

    # We create another application in the same job season
    applications = json.loads(apply_external_posting(user_id, url, position, company, resume,
                                                     date_posted, deadline))

    assert len(applications) == 2
    assert applications[0]['resume'] == applications[1]['resume']
    assert applications[0]['status'] == applications[1]['status'] == "applied"


def test__update_status_empty_string(test_teardown):
    """
    Failure scenario: Empty status should give an error
    """
    user_id = 1

    # We create an application in the DB
    applications = json.loads(apply_external_posting(user_id, url, position, company, resume,
                                                     date_posted, deadline))

    # We update the status of this application
    new_status = ""
    with pytest.raises(Exception) as e:
        update_status_external_posting(applications[0]['id'], new_status)


def test__apply(test_teardown):
    """
    Regular scenario for applying to external postings
    """
    user_id = 1
    
    # We create an application in the DB
    apply_external_posting(user_id, url, position, company, resume,
                           date_posted, deadline)
    applications = json.loads(get_applications_external(user_id))

    assert applications[0]['user_id'] == user_id
    assert applications[0]['is_inhouse_posting'] == False
    assert applications[0]['url'] == url
    assert applications[0]['position'] == position
    assert applications[0]['company'] == company
    assert applications[0]['resume'] == resume


def test__update_status(test_teardown):
    """
    Regular scenario for updating a status
    """
    user_id = 1
    new_status = "new!"

    # We create an application in the DB
    applications = json.loads(apply_external_posting(user_id, url, position, company, resume,
                                                     date_posted, deadline))
    updated_applications = json.loads(update_status_external_posting(applications[0]['id'], new_status))

    assert applications[0]['status'] != new_status
    assert updated_applications[0]['status'] == new_status
    assert updated_applications[0]['id'] == applications[0]['id']
