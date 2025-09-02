from datetime import date

class Doctor:
    def __init__(self, name, performable_duties, working_days, working_wknd, num_ef = None, dates_of_leave=None):
        self.name = name
        self.performable_duties = performable_duties # List of duties doctor can perform
        self.working_days = working_days # List of days doctor works e.g. [Monday, Wednesday ...]
        self.working_wknd = working_wknd # Boolean
        self.num_ef =  num_ef # Integer of doctors that only do some efs
        self.dates_of_leave = dates_of_leave if dates_of_leave is not None else [] # Tuple of datetime.date objects of when leave starts and when leave ends


    def is_available_on(self, check_date, day_name):
        for leave_start, leave_end in self.dates_of_leave:
            if leave_start <= check_date <= leave_end:
                return False

        if day_name in self.working_days:
            return True
        elif day_name == "Saturday" or day_name == "Sunday":
            if self.working_wknd:
                return True
            else:
                return False

    def change_dates_of_leave(self, start_of_leave, end_of_leave):
        self.dates_of_leave = [(start_of_leave, end_of_leave)]

