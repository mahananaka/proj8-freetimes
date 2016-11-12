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
    Testing interpret time function
    """

    sample = "11:20pm"
    arw_output = arrow.get(sample,"h:mma").replace(tzinfo=tz.tzlocal(),year=2016).isoformat()
    assert interpret_time(sample) == arw_output
    assert interpret_time(sample,"h:mma") == arw_output    

def test_interpret_date():
    """
    Testing intrepret_date function
    """
    sample = "11/15/2016"
    arw_output = arrow.get(sample,"MM/DD/YYYY").replace(tzinfo=tz.tzlocal()).isoformat()

    assert interpret_date(sample) == arw_output #text default value for format
    assert interpret_date("2016/11/15","YYYY/MM/DD") == arw_output #test a supplied date format
    assert interpret_date("15-2016-11","DD-YYYY-MM") == arw_output #test with a very weird date format

def test_in_time_frame():
    """
    Testing in_time_frame function
    """
    fmt = "h:mma"
    start = interpret_time("11:00am",fmt)
    end = interpret_time("1:00pm",fmt)

    #Each case of how the time of events call fall around the boundry times provided by user    
    assert in_time_frame(start,end,interpret_time("10:00am",fmt),interpret_time("10:30am",fmt)) == False
    assert in_time_frame(start,end,interpret_time("12:00pm",fmt),interpret_time("2:00pm",fmt)) == True
    assert in_time_frame(start,end,interpret_time("10:00am",fmt),interpret_time("2:00pm",fmt)) == True
    assert in_time_frame(start,end,interpret_time("10:00am",fmt),interpret_time("12:00pm",fmt)) == True
    assert in_time_frame(start,end,interpret_time("12:00pm",fmt),interpret_time("12:30pm",fmt)) == True
    assert in_time_frame(start,end,interpret_time("11:00am",fmt),interpret_time("1:00pm",fmt)) == True