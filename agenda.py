"""An Agenda is a list-like container of Appt (appointment).

   Author: FIXME for CIS 210, U. Oregon

   Each Appt has a date, a start time, an end time, and
   a textual description.   They can be converted to and
   from strings, using the from_string class method and the __str__
   method.  An Agenda can be read from a file using the
   from_file class method.  Intersecting Agendas produces
   a new Agenda whose Appts are periods that are in the overlap
   of Appts in the first and second Agenda.
   

"""

import datetime
import dateutil.parser as dt
class Appt:

    """
    A single appointment, starting on a particular
    date and time, and ending at a later time the same day.
    """
    
    def __init__(self, day, begin, end, desc): #changed
        """Create an appointment on date
        from begin time to end time.
        
        Arguments:
            day:   A datetime.date object.  The appointment occurs this day.
            begin: A datetime.time object.  When the appointment starts. 
            end:  A datetime.time object, 
                after begin.                When the appointments ends.
            desc: A string describing the appointment
            
        Raises: 
        	ValueError if appointment ends before it begins
        	
        Example:
            Appt( datetime.date(2012,12,1),
                datetime.time(16,30),
                datetime.time(17,45))
            (December 1 from 4:30pm to 5:45pm)
        """
        self.begin = datetime.datetime.combine(day, begin)
        self.end = datetime.datetime.combine(day, end)
        if begin >= end :
            raise ValueError("Appointment end must be after begin")
        self.desc = desc
        return

    @classmethod
    def from_iso_date(cls, start, finish, desc):
        begin = dt.parse(start)
        end = dt.parse(finish)

        if begin.date() != end.date():
            raise ValueError("The start and finish should have the same dates.")

        result = Appt(begin.date(), begin.time(), end.time(), desc)
        return result

    # @classmethod
    # def from_string(cls, txt):
    #     """Factory parses a string to create an Appt"""
    #     fields = txt.split("|")
    #     if len(fields) != 2:
    #         raise ValueError("Appt literal requires exactly one '|' before description")
    #     timespec = fields[0].strip()
    #     desc = fields[1].strip()
    #     fields = timespec.split()
    #     if len(fields) != 3:
    #         raise ValueError("Appt literal must start with date, time, time, separated by blanks")
    #     appt_date_text = fields[0]
    #     appt_begin_text = fields[1]
    #     appt_end_text = fields[2]
    #     fields = appt_date_text.split(".")
    #     try:
    #         year = int(fields[0].strip())
    #         month = int(fields[1].strip())
    #         day = int(fields[2].strip())
    #     except:
    #         raise ValueError("Date in Appt literal should be 9999.99.99 (Year.Month.Day)")

    #     ### 
    #     date = datetime.date(year,month,day)
    #     begin = datetime.datetime.strptime(appt_begin_text, "%H:%M").time()
    #     end =   datetime.datetime.strptime(appt_end_text, "%H:%M").time()

    #     result = Appt(date, begin, end, desc)
    #     return result

    def start_isoformat(self):
        return self.begin.isoformat()
        
    def end_isoformat(self):
        return self.end.isoformat()

    def __lt__(self, other):
        """Does this appointment finish before other begins?
        
        Arguments:
        	other: another Appt
        Returns: 
        	True iff this Appt is done by the time other begins.
        """
        return self.end <= other.begin
        
    def __gt__(self, other):
        """Does other appointment finish before this begins?
        
        Arguments:
        	other: another Appt
        Returns: 
        	True iff other is done by the time this Appt begins
        """
        return other < self
        
    def overlaps(self, other):
        """Is there a non-zero overlap between this appointment
        and the other appointment?
		Arguments:
            other is an Appt
        Returns:
            True iff there exists some duration (greater than zero)
            between this Appt and other. 
        """
        return  not (self < other or other < self)
            
    def intersect(self, other, desc=""):
        """Return an appointment representing the period in
        common between this appointment and another.
        Requires self.overlaps(other).
        
		Arguments: 
			other:  Another Appt
			desc:  (optional) description text for this appointment. 

		Returns: 
			An appointment representing the time period in common
			between self and other.   Description of returned Appt 
			is copied from this (self), unless a non-null string is 
			provided as desc. 
        """
        if desc=="":
            desc = self.desc
        assert(self.overlaps(other))
        # We know the day must be the same. 
        # Find overlap of times: 
        #   Later of two begin times, earlier of two end times
        begin_time = max(self.begin.time(), other.begin.time())
        end_time = min(self.end.time(), other.end.time())
        return Appt(self.begin.date(), begin_time, end_time, desc)

    def union(self, other, desc=""):
        """Return an appointment representing the combined period in
        common between this appointment and another.
        Requires self.overlaps(other).
        
		Arguments: 
			other:  Another Appt
			desc:  (optional) description text for this appointment. 

		Returns: 
			An appointment representing the time period spanning
                        both self and other.   Description of returned Appt 
			is concatenation of two unless a non-null string is 
			provided as desc. 
        """
        if desc=="":
            desc = self.desc + " " + other.desc
        assert(self.overlaps(other))
        # We know the day must be the same. 
        # Find overlap of times: 
        #   Earlier of two begin times, later of two end times
        begin = min(self.begin, other.begin)
        end = max(self.end, other.end)
        return Appt(self.begin.date(), begin.time(), end.time(), desc)

    def __str__(self):
        """String representation of appointment.
        Example:
            2012.10.31 13:00 13:50 | CIS 210 lecture
            
        This format is designed to be easily divided
        into parts:  Split on '|', then split on whitespace,
        then split date on '.' and times on ':'.
        """
        daystr = self.begin.date().strftime("%Y.%m.%d ")
        begstr = self.begin.strftime("%H:%M ")
        endstr = self.end.strftime("%H:%M ")
        return daystr + begstr + endstr + "| " + self.desc

class Agenda:
    """An Agenda is essentially a list of appointments,
    with some agenda-specific methods.
    """

    def __init__(self):
        """An empty agenda."""
        self.appts = [ ]
        
    # @classmethod
    # def from_file(cls, f):
    #     """Factory: Read an agenda from a file.
        
    #     Arguments: 
    #         f:  A file object (as returned by io.open) or
    #            an object that emulates a file (like stringio). 
    #     returns: 
    #         An Agenda object
    #     """
    #     agenda = cls()
    #     for line in f:
    #         line = line.strip()
    #         if line == "" or line.startswith("#"):
    #             # Skip blank lines and comments
    #             pass
    #         else: 
    #             try: 
    #                 agenda.append(Appt.from_string(line))
    #             except ValueError as err: 
    #                 print("Failed on line: ", line)
    #                 print(err)
    #     return agenda

    def append(self,appt):
        """Add an Appt to the agenda."""
        self.appts.append(appt)

    # def merge_agenda(self, other):
    #     for appt in other.appts:
    #         self.append(appt)
        
    #     self.appts.sort(lambda ap: ap.begin)



    def get_date(self):
        """Returns the date of the first appt in the agenda"""
        if len(self.appts) < 1:
            return None
        else:
            return self.appts[0].begin.isoformat()

    def intersect(self,other,desc=""): 
        """Return a new agenda containing appointments
        that are overlaps between appointments in this agenda
        and appointments in the other agenda.

        Titles of appointments in the resulting agenda are
        taken from this agenda, unless they are overridden with
        the "desc" argument.

        Arguments:
           other: Another Agenda, to be intersected with this one
           desc:  If provided, this string becomes the title of
                all the appointments in the result.
        """
        default_desc = (desc == "")
        result = Agenda()
        for thisappt in self.appts:
            if default_desc: 
                desc = thisappt.desc
            for otherappt in other.appts:
                if thisappt.overlaps(otherappt):
                    result.append(thisappt.intersect(otherappt,desc))
        
        return result

    def normalize(self):
        """Merge overlapping events in an agenda. For example, if 
        the first appointment is from 1pm to 3pm, and the second is
        from 2pm to 4pm, these two are merged into an appt from 
        1pm to 4pm, with a combination description.  
        After normalize, the agenda is in order by date and time, 
        with no overlapping appointments.
        """
        if len(self.appts) == 0:
            return

        ordering = lambda ap: ap.begin
        self.appts.sort(key=ordering)

        normalized = [ ]
        # print("Starting normalization")
        cur = self.appts[0]  
        for appt in self.appts[1:]:
            if appt > cur:
                # Not overlapping
                # print("Gap - emitting ", cur)
                normalized.append(cur)
                cur = appt
            else:
                # Overlapping
                # print("Merging ", cur, "\n"+
                #      "with    ", appt)
                cur = cur.union(appt)
                # print("New cur: ", cur)
        # print("Last appt: ", cur)
        normalized.append(cur)
        self.appts = normalized

    def normalized(self):
        """
        A non-destructive normalize
        (like "sorted(l)" vs "l.sort()").
        Returns a normalized copy of this agenda.
        """
        copy = Agenda()
        copy.appts = self.appts
        copy.normalize()
        return copy
        
    def complement(self, freeblock):
        """Produce the complement of an agenda
        within the span of a timeblock represented by 
        an appointment.  For example, 
        if this agenda is a set of appointments, produce a 
        new agenda of the times *not* in appointments in 
        a given time period.
        Args: 
           freeblock: Looking  for time blocks in this period 
               that are not conflicting with appointments in 
               this agenda.
        Returns: 
           A new agenda containing exactly the times that 
           are within the period of freeblock and 
           not within appointments in this agenda. The 
           description of the resulting appointments comes
           from freeblock.desc.
        """
        copy = self.normalized()
        comp = Agenda()
        day = freeblock.begin.date()
        desc = freeblock.desc
        cur_time = freeblock.begin
        for appt in copy.appts:
            if appt < freeblock:
                continue
            if appt > freeblock:
                if cur_time < freeblock.end:
                    comp.append(Appt(day,cur_time.time(),freeblock.end.time(), desc))
                    cur_time = freeblock.end
                break
            if cur_time < appt.begin:
                # print("Creating free time from", cur_time, "to", appt.begin)
                comp.append(Appt(day, cur_time.time(), appt.begin.time(), desc))
            cur_time = max(appt.end,cur_time)

        if cur_time < freeblock.end:
            # print("Creating final free time from", cur_time, "to", freeblock.end)
            comp.append(Appt(day, cur_time.time(), freeblock.end.time(), desc))
        return comp



    def __len__(self):
        """Number of appointments, callable as built-in len() function"""
        return len(self.appts)

    def __iter__(self):
        """An iterator through the appointments in this agenda."""
        return self.appts.__iter__()

    def __str__(self):
        """String representation of a whole agenda"""
        rep = ""
        for appt in self.appts:
            rep += str(appt) + "\n"
        return rep[:-1]

    def __eq__(self,other):
        """Equality, ignoring descriptions --- just equal blocks of time"""
        if len(self.appts) != len(other.appts):
            return False
        for i in range(len(self.appts)):
            mine = self.appts[i]
            theirs = other.appts[i]
            if not (mine.begin == theirs.begin and
                    mine.end == theirs.end):
                return False
        return True


#########################
#  Self-test invoked when module is run
#  as main program. 
#########################
    
# from test_harness import *
# import io
# def selftest_appt():
#     """Simple smoke test for Appt class."""
#     sample = Appt(datetime.date(2012, 10, 31),
#                   datetime.time(14, 30), datetime.time(15, 45),
#                   "Sample appointment")
#     testEQ("Create and format",str(sample),
#            "2012.10.31 14:30 15:45 | Sample appointment") 
    
#     earlier = Appt(datetime.date(2012, 10, 31),
#                     datetime.time(13, 30), datetime.time(14,30), 
#                     "Before my appt")
#     later = Appt(datetime.date(2012, 10, 31),
#                   datetime.time(16,00), datetime.time(21,00), "Long dinner")
    
#     testEQ("Strictly before is '<'", earlier < later, True)
#     testEQ("Strictly after is '>'", later > earlier, True)
#     testEQ("Not earlier than itself", earlier < earlier, False)
#     testEQ("Not later than itself", earlier > later, False)
    
#     testEQ("Earlier doesn't overlap later", earlier.overlaps(later), False) 
#     testEQ("Later doesn't overlap earlier", later.overlaps(earlier), False)
    
#     conflict = Appt(datetime.date(2012, 10, 31), 
#                     datetime.time(13, 45), datetime.time(16,00),
#         "Conflicting appt")

#     testEQ("Should overlap", sample.overlaps(conflict), True)
#     testEQ("Opposite overlap", conflict.overlaps(sample), True)
#     overlap = sample.intersect(conflict)
#     testEQ("Expected intersection", str(overlap), 
#            "2012.10.31 14:30 15:45 | Sample appointment")
#     overlap = conflict.intersect(sample)
#     testEQ("Expected intersection", str(overlap), 
#            "2012.10.31 14:30 15:45 | Conflicting appt")
#     overlap = conflict.intersect(sample,"New desc")
#     testEQ("Expected intersection", str(overlap), 
#            "2012.10.31 14:30 15:45 | New desc")

#     text = "2012.10.31 14:30 15:45 | from text"
#     from_text = Appt.from_string(text)
#     testEQ("String <-> Appt",text, str(from_text))
#     def die():
#        Appt.from_string("2012.10.31 15:45 14:30 | time traveler")
#     testRaise("Time order error", ValueError, die)       
       

# def selftest_agenda():
#     """Simple smoke test for Agenda class."""

#     keiko_agtxt="""# Free times for Keiko on December 1
#            2012.12.1 07:00 08:00  | Possible breakfast meeting
#            2012.12.1 10:00 12:00  | Late morning meeting
#            2012.12.1 14:00 18:00  | Afternoon meeting
#          """

#     kevin_agtxt="""2012.11.30 09:00 14:00 | I have an afternoon commitment on the 30th
#           2012.12.1  09:00 15:00 | I prefer morning meetings
#           # Kevin always prefers morning, but can be available till 3, except for 
#           # 30th of November.
#           """

#     emanuela_agtxt = """
#     2012.12.1 12:00 14:00 | Early afternoon
#     2012.12.1 16:00 18:00 | Late afternoon into evening
#     2012.12.2 8:00 17:00 | All the next day
#     """
    
#     keiko_ag = Agenda.from_file(io.StringIO(keiko_agtxt))
#     kevin_ag = Agenda.from_file(io.StringIO(kevin_agtxt))
#     emanuela_ag = Agenda.from_file(io.StringIO(emanuela_agtxt))

#     keiko_kevin = keiko_ag.intersect(kevin_ag)
#     kk = ("2012.12.01 10:00 12:00 | Late morning meeting\n" +
#          "2012.12.01 14:00 15:00 | Afternoon meeting")
#     kkactual = str(keiko_kevin)
#     testEQ("Keiko and Kevin", kkactual.strip(), kk.strip())

#     kevin_emanuela = kevin_ag.intersect(emanuela_ag)
#     ke = "2012.12.01 12:00 14:00 | I prefer morning meetings"
#     keactual = str(kevin_emanuela)
#     testEQ("Kevin and Emanuela", keactual, ke)

#     everyone = keiko_kevin.intersect(emanuela_ag)
#     testEQ("No overlap of all three", len(everyone), 0)

# def selftest2_agenda():

#     print("""
#     **********************************
#     *** Smoke test Agenda addenda   **
#     *** normalization and complement**
#     ********************************""")
    
#     """Additional tests for agenda normalization and complement."""
#     # What could go wrong in sorting? 
#     keiko_agtxt="""2013.12.2 12:00 14:00 | Late lunch
#                    2013.12.1 13:00 14:00 | Sunday brunch
#                    2013.12.2 08:00 15:00 | Long long meeting
#                    2013.12.2 15:00 16:00 | Coffee after the meeting"""
#     keiko_ag = Agenda.from_file(io.StringIO(keiko_agtxt))

#     # Torture test for normalization
#     day_in_life_agtxt = """
# # A torture-test agenda.  I am seeing a lot of code 
# # that may not work well with sequences of three or more
# # appointments that need to be merged.  Here's an agenda
# # with such a sequence.  Also some Beatles lyrics that have
# # been running through my head.  
# # 
# 2013.11.26 09:00 10:30 | got up
# 2013.11.26 10:00 11:30 | got out of bed
# 2013.11.26 11:00 12:30 | drug a comb across my head
# 2013.11.26 12:00 13:30 | on the way down stairs I had a smoke
# 2013.11.26 13:00 14:30 | and somebody spoke
# 2013.11.26 14:00 15:30 | and I went into a dream
# #
# # A gap here, from 15:30 to 17:00
# # 
# 2013.11.26 17:00  18:30 | he blew his mind out in a car
# 2013.11.26 18:00  19:30 | hadn't noticed that the lights had changed
# 2013.11.26 19:00  20:30 | a crowd of people stood and stared
# #
# # A gap here, from 20:30 to 21:00
# #
# 2013.11.26 21:00 22:30 | they'd seen his face before
# 2013.11.26 22:00 23:00 | nobody was really sure ..."""
#     day_in_life = Agenda.from_file(io.StringIO(day_in_life_agtxt))
#     day_in_life.normalize()
#     # How are we going to test this?  I want to ignore the text descriptions.
#     # Defined __eq__ method in Agenda just for this
#     should_be_txt = """
#     2013.11.26 09:00 15:30 | I read the news today oh, boy
#     2013.11.26 17:00 20:30 | about a lucky man who made the grade
#     2013.11.26 21:00 23:00 | and though the news was rather sad
#     """
#     should_be_ag = Agenda.from_file(io.StringIO(should_be_txt))
#     testEQ("Torture test normalized",day_in_life,should_be_ag)

#     # Start with the simplest cases of "complement"
#     simple_agtxt = """2013.12.01 12:00 14:00 | long lunch"""
#     simple_ag = Agenda.from_file(io.StringIO(simple_agtxt))
    
#     # Different day - should have no effect
#     tomorrow = Appt.from_string("""2013.12.02 11:00 15:00 | tomorrow""")
#     simple_ag = simple_ag.complement(tomorrow)
#     testEQ("Yesterday's appts don't matter",str(simple_ag).strip(),
#            """2013.12.02 11:00 15:00 | tomorrow""")
#     # And the freeblock should not be altered
#     testEQ("Not clobber freeblock",str(tomorrow),
#            """2013.12.02 11:00 15:00 | tomorrow""")
    
#     # Freeblock completely covered
#     simple_agtxt = """2013.12.01 12:00 14:00 | long lunch"""
#     simple_ag = Agenda.from_file(io.StringIO(simple_agtxt))
#     lunch = Appt.from_string("""2013.12.01 12:30 13:30 | lunch""")
#     simple_ag = simple_ag.complement(lunch)
#     testEQ("Completely blocked freeblock",str(simple_ag).strip(),"")
#     # And the freeblock should not be altered
#     testEQ("Not clobber freeblock 2",str(lunch),
#            """2013.12.01 12:30 13:30 | lunch""")
    
#     # Freeblock different times same day
#     simple_agtxt = """2013.12.01 12:00 14:00 | long lunch"""
#     simple_ag = Agenda.from_file(io.StringIO(simple_agtxt))
#     dinner = Appt.from_string("""2013.12.01 19:30 20:30 | dinner""")
#     simple_ag = simple_ag.complement(dinner)
#     testEQ("Freeblock later in day",str(simple_ag).strip(),
#            """2013.12.01 19:30 20:30 | dinner""")
#     #
#     # More complex agendas - try with two appointments
#     #
#     simple_agtxt = """
#     2013.12.01 9:00 11:00 | morning meeting
#     2013.12.01 13:00 14:00 | afternoon meeting"""
#     # Cover first part first appt
#     simple_ag = Agenda.from_file(io.StringIO(simple_agtxt))
#     part_cover_first = Appt.from_string("2013.12.01 08:30 09:30 | morning coffee")
#     simple_ag = simple_ag.complement(part_cover_first)
#     testEQ("Freeblock partly covers first appt start only",
#            str(simple_ag).strip(), "2013.12.01 08:30 09:00 | morning coffee")
#     # Cover last part first appt
#     simple_ag = Agenda.from_file(io.StringIO(simple_agtxt))
#     part_cover_first = Appt.from_string("2013.12.01 09:30 11:30 | morning coffee")
#     simple_ag = simple_ag.complement(part_cover_first)
#     testEQ("Freeblock partly covers first appt end only",
#            str(simple_ag).strip(), "2013.12.01 11:00 11:30 | morning coffee")
#     # Cover first part second appt
#     simple_ag = Agenda.from_file(io.StringIO(simple_agtxt))
#     part_cover_first = Appt.from_string("2013.12.01 12:30 13:30 | afternoon coffee")
#     simple_ag = simple_ag.complement(part_cover_first)
#     testEQ("Freeblock partly covers second appt start only",
#            str(simple_ag).strip(), "2013.12.01 12:30 13:00 | afternoon coffee")
#     # Cover last part second appt
#     simple_ag = Agenda.from_file(io.StringIO(simple_agtxt))
#     part_cover_first = Appt.from_string("2013.12.01 13:30 14:30 | afternoon coffee")
#     simple_ag = simple_ag.complement(part_cover_first)
#     testEQ("Freeblock partly covers second appt end only",
#            str(simple_ag).strip(), "2013.12.01 14:00 14:30 | afternoon coffee")
#     # Cover middle part two appts
#     simple_ag = Agenda.from_file(io.StringIO(simple_agtxt))
#     part_cover_first = Appt.from_string("2013.12.01 10:30 13:30 | mid-day")
#     simple_ag = simple_ag.complement(part_cover_first)
#     testEQ("Freeblock partly covers two appts and gap",
#            str(simple_ag).strip(), "2013.12.01 11:00 13:00 | mid-day")
#     # Extend across two appts
#     simple_ag = Agenda.from_file(io.StringIO(simple_agtxt))
#     part_cover_first = Appt.from_string("2013.12.01 08:00 15:00 | most of day")
#     simple_ag = simple_ag.complement(part_cover_first)
#     testEQ("Freeblock fully covers two appts and gap",
#            str(simple_ag).strip(), "2013.12.01 08:00 09:00 | most of day" +
#            "\n" + "2013.12.01 11:00 13:00 | most of day" + 
#            "\n" + "2013.12.01 14:00 15:00 | most of day")

# if __name__ == "__main__":
#     selftest_appt()
#     selftest_agenda()
#     selftest2_agenda()
        

    
    
    
    
    
