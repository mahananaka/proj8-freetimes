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
    end = "11/15/2016 6:00pm"
    decr = "Test Appt"
    start_as_iso = arrow.get(start,"MM/DD/YYYY h:mma").replace(tzinfo=tz.tzlocal()).isoformat()
    end_as_iso = arrow.get(end,"MM/DD/YYYY h:mma").replace(tzinfo=tz.tzlocal()).isoformat()
    output = Appt.from_iso_date(start_as_iso.isoformat(),end_as_iso.isoformat(),decr)
    
    assert output.start_isoformat() == start_as_iso
    assert output.end_isoformat() == end_as_iso
    