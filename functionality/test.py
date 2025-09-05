from doctor_roster import all_doctors
from month_logic import generate_working_days
from tabulate import tabulate


doctors = all_doctors()
working_days, doctor_counts, weekends = generate_working_days(doctors)


# Create list of table rows
table = []

for i in range(len(doctor_counts)):
    day = working_days[i]
    doctors_on_day = doctor_counts[i]
    doctor_names = ", ".join([doctor.name for doctor in doctors_on_day])
    duties = day.return_duties().strip()
    ef_doctor = day.doctor_on_ef.name if day.doctor_on_ef else "N/A"

    table.append([
        day.date.strftime('%Y-%m-%d'),
        duties,
        doctor_names,
        ef_doctor
    ])

# Print the table
headers = ["Date", "Duties Assigned", "Doctors Available", "ΕΦΗΜΕΡΙΑ"]
print(tabulate(table, headers=headers, tablefmt="grid"))

print("\n")
print("WEEKENDS")
for day, weekend in weekends.items():
    print(day.strftime('%Y-%m-%d ') + weekend.doctor_assigned.name)


