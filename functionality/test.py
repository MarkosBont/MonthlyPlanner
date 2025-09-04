from doctor_roster import all_doctors
from datetime import date
from functionality.classes.doctor import Doctor
from month_logic import generate_working_days
from functionality.classes.weekend import Weekend


doctors = all_doctors()



working_days, doctor_counts, weekends = generate_working_days(doctors)




for i in range(len(doctor_counts)):
    day = working_days[i]
    doctors_on_day = doctor_counts[i]
    doctor_names = [doctor.name for doctor in doctors_on_day]
    print("Date: " + day.date.strftime('%Y-%m-%d') +
          "\nDuties assigned: \n" + day.return_duties() +
          "Doctors: " + ", ".join(doctor_names) + "\n")

print("WEEKENDS")
for day, weekend in weekends.items():
    print(day.strftime('%Y-%m-%d ') + weekend.doctor_assigned.name)


