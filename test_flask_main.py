"""
Nose tests for flask_main.py
"""
# Date handling 
import arrow # Replacement for datetime, based on moment.js
import datetime # But we still need time
from dateutil import tz  # For interpreting local times

# modules we are testing
from flask_main import interpret_time, interpret_date, in_time_frame
from flask_main import same_date, combine_date_time
from agenda import Appt, Agenda

def test_interpret_time():
    """
    Testing interspret time function
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

"""
Everything below here is the new tests added for proj8
"""
def test_same_date():
    """
    Testing same_date function
    """
    sample = "11/15/2016"
    test_input1 = arrow.get(sample,"MM/DD/YYYY").replace(tzinfo=tz.tzlocal()).isoformat()
    test_input2 = arrow.get(test_input1).replace(days=+1).isoformat()

    assert same_date(test_input1,test_input2) == False
    assert same_date(test_input1,test_input1) == True
    assert same_date(test_input2,test_input2) == True
    assert same_date(test_input1,arrow.get(test_input1).replace(hours=+6).isoformat()) == True

def test_combine_date_time():
    """
    Testing combine_date_time()
    This should take an arrow date and time object and mash them together
    """

    a_date = "11/15/2016 8:15am"
    a_time = "11/20/2016 1:30pm" #but on a different date
    test_input1 = arrow.get(a_date,"MM/DD/YYYY h:mma").replace(tzinfo=tz.tzlocal()).isoformat()
    test_input2 = arrow.get(a_time,"MM/DD/YYYY h:mma").replace(tzinfo=tz.tzlocal()).isoformat()
    desired_output = arrow.get("11/15/2016 1:30pm","MM/DD/YYYY h:mma").replace(tzinfo=tz.tzlocal()).isoformat()

    assert combine_date_time(test_input1,test_input2) == desired_output
