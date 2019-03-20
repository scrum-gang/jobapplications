import pytest
import os
import sys
sys.path.insert(0, os.getcwd())

from tables import Application, Inhouse, External, InterviewQuestion


@pytest.fixture()
def test_teardown():
    InterviewQuestion.query.delete()
    Inhouse.query.delete()
    External.query.delete()
    Application.query.delete()
