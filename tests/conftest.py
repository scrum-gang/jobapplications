import pytest
import os
import sys
sys.path.insert(0, os.getcwd())

from tables import Application, Inhouse, External, Season


@pytest.fixture()
def test_teardown():
    Inhouse.query.delete()
    External.query.delete()
    Application.query.delete()
    Season.query.delete()
