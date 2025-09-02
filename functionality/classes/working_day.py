class WorkingDay:
    def __init__(self, date, day_name, doctors_on_leave = None, doctor_on_ef = None):
        self.date = date
        self.day_name = day_name
        self.doctor_duties = {}
        self.doctors_on_leave = doctors_on_leave
        self.doctor_on_ef = doctor_on_ef

    def add_duties(self, doctor, duty):
        if doctor not in self.doctor_duties:
            self.doctor_duties[doctor] = []
        self.doctor_duties[doctor].append(duty)

    def add_doctor_on_leave(self, doctor):
        if self.doctors_on_leave is None:
            self.doctors_on_leave = [doctor]
        else:
            self.doctors_on_leave.append(doctor)

    def add_doctor_on_ef(self, doctor):
        self.doctor_on_ef = doctor

    def return_duties(self):
        dictionary = self.doctor_duties
        text = ""
        for doctor, duty in dictionary.items():
            text += f"{doctor.name}: {duty}\n"

        return text
