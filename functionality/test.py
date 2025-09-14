from doctor_roster import all_doctors
from month_logic import generate_working_days
from tabulate import tabulate


doctors = all_doctors()
working_days, doctor_counts, weekends = generate_working_days(doctors)


# Create list of table rows
table = []

# Print weekday assignments
for i in range(len(doctor_counts)):
    day = working_days[i]
    doctors_on_day = doctor_counts[i]
    doctor_names = ", ".join([doctor.name for doctor in doctors_on_day])
    duties = day.return_duties().strip()
    ef_doctor = day.doctor_on_ef.name if day.doctor_on_ef else "N/A"

    print(f"{day.date.strftime('%Y-%m-%d')}")
    print(f"Duties Assigned:\n{duties}")
    print(f"Doctors Available: {doctor_names}")
    print(f"Νight Doctor (ΕΦΗΜΕΡΙΑ): {ef_doctor}")
    print("-" * 40)

# Print weekends
print("\nWEEKENDS")
for day, weekend in weekends.items():
    print(f"{day.strftime('%Y-%m-%d')}: {weekend.doctor_assigned.name}")


