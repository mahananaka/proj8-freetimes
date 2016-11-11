"""
Nose tests for flask_main.py
"""
# Date handling 
import arrow # Replacement for datetime, based on moment.js
import datetime # But we still need time
from dateutil import tz  # For interpreting local times

# module we are testing
from flask_main import humanize_arrow_date
from flask_main import get_memos
from flask_main import insert_memo
from flask_main import delete_memo


def test_humanize_arrow_date():
    """
    Testing Humanize
    """
    curDateTime = arrow.utcnow().to('local')

    assert humanize_arrow_date(curDateTime) == "Today"
    assert humanize_arrow_date(curDateTime.replace(days=+1)) == "Tomorrow"
    assert humanize_arrow_date(curDateTime.replace(days=-1)) == "Yesterday"

def test_insert_memo():
    """
    Testing insertion into db
    """
    assert insert_memo("02/30/2016","Testing a failed insert") == False
    assert insert_memo("11/12/2016","This entry is created by nose") == True

def test_get_memos():
    """
    Testing memos retrieval
    """
    records = get_memos()

    assert len(records) > 0 #We inserted in last test so this should not be 0

    #veryify the proper form of the dict
    for entry in records:
        assert entry['_id'] is not None
        assert entry['date'] is not None
        assert entry['text'] is not None

def test_get_memos():
    """
    Testing memo delete
    """
    key = {'text':'This entry is created by nose'} #This entry exists if insertion testing passed.
    foundAndDelted = False

    for record in collection.find(key):
        collection.remove({'_id':record['_id']})
        foundAndDelted = True

    assert foundAndDelted == True
