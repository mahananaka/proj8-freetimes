"""
Nose tests for flask_main.py
"""
# Date handling 
import arrow # Replacement for datetime, based on moment.js
import datetime # But we still need time
from dateutil import tz  # For interpreting local times

# modules we are testing
from agenda import Appt, Agenda

"""
The testing done here is focused on my modifications to agenda.py since
the baseline code is heavily tested within the file by the original author.
"""

def test_appt():
    """
    Testing intrepret_date function
    """
    start = "11/15/2016 5:42am"
    end = "11/16/2016 6:00pm"
    decr = "Test Appt"
    start_as_iso = arrow.get(start,"MM/DD/YYYY h:mma").replace(tzinfo=tz.tzlocal()).isoformat()
    end_as_iso = arrow.get(end,"MM/DD/YYYY h:mma").replace(tzinfo=tz.tzlocal()).isoformat()
    
    assert Appt.from_iso_date(start_as_iso,end_as_iso,decr)
    #assert Appt.from_iso_date(sample) == arw_output #text default value for format
    