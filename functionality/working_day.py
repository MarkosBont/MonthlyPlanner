class WorkingDay:
    def __init__(self, date, day_name, doctor_duties = None, doctors_on_leave = None, doctor_on_ef = None):
        self.date = date
        self.day_name = day_name
        self.doctor_duties = doctor_duties
        self.doctors_on_leave = doctors_on_leave
        self.doctor_on_ef = doctor_on_ef

    def add_duties(self, doctor, duty):
        if self.doctor_duties is None:
            self.doctor_duties = {doctor: duty}
        else:
            self.doctor_duties[doctor] += duty

    def add_doctor_on_leave(self, doctor):
        if self.doctors_on_leave is None:
            self.doctors_on_leave = [doctor]
        else:
            self.doctors_on_leave.append(doctor)

    def add_doctor_on_ef(self, doctor):
        self.doctor_on_ef = doctor