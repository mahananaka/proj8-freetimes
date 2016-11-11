"""
Nose tests for flask_main.py
"""
# Date handling 
import arrow # Replacement for datetime, based on moment.js
import datetime # But we still need time
from dateutil import tz  # For interpreting local times

# module we are testing
from flask_main import interpret_time
from flask_main import interpret_date
from flask_main import in_time_frame

def test_interpret_time():
    """
    Testing Humanize
    """
    #curDateTime = arrow.utcnow().to('local')

    #assert humanize_arrow_date(curDateTime) == "Today"
    #assert humanize_arrow_date(curDateTime.replace(days=+1)) == "Tomorrow"
    #assert humanize_arrow_date(curDateTime.replace(days=-1)) == "Yesterday"

def test_interpret_date():
    """
    Testing insertion into db
    """
    #assert insert_memo("02/30/2016","Testing a failed insert") == False
    #assert insert_memo("11/12/2016","This entry is created by nose") == True

def test_in_time_frame():
    """
    Testing memos retrieval
    """
    #records = get_memos()

    #assert len(records) > 0 #We inserted in last test so this should not be 0

    #veryify the proper form of the dict
    #for entry in records:
    #    assert entry['_id'] is not None
    #    assert entry['date'] is not None
    #    assert entry['text'] is not None
