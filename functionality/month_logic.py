from functionality.classes.working_day import WorkingDay
import calendar
from datetime import date
from month_logic_functions import assign_duties
from functionality.classes.weekend import Weekend
from collections import defaultdict


def generate_working_days(doctors):

    dr_p = next(d for d in doctors if d.name == "P")
    dr_m = next(d for d in doctors if d.name == "M")
    dr_k = next(d for d in doctors if d.name == "K")
    dr_q = next(d for d in doctors if d.name == "Q")
    dr_s = next(d for d in doctors if d.name == "S")
    dr_z = next((d for d in doctors if d.name == "Z"), None)
    dr_y = next(d for d in doctors if d.name == "Y")
    dr_g = next(d for d in doctors if d.name == "G")
    dr_i = next(d for d in doctors if d.name == "I")
    dr_n = next(d for d in doctors if d.name == "N")


    working_days = []
    weekends = {}
    doctor_counts = []

    today = date.today()

    weekend_order = [dr_p, dr_s, dr_m, dr_q, dr_k, dr_z] if today >= date(2025, 12, 1) else [dr_p, dr_s, dr_m, dr_q, dr_k]
    current_weekend_doctor_index = 3

    if today.month == 12:
        next_month = 1
        year = today.year + 1
    else:
        next_month = today.month + 1
        year = today.year

    cal = calendar.Calendar()
    weeks = cal.monthdatescalendar(year, next_month)

    for week in weeks:
        for day in week:

            if day.month == next_month:
                day_name = day.strftime('%A')
                if day_name == "Saturday":
                    for offset in range(1, len(weekend_order)):
                        i = (current_weekend_doctor_index + offset) % len(weekend_order)
                        doctor = weekend_order[i]
                        if doctor.is_available_on(day, day_name):
                            weekend = Weekend(day.isoformat(), doctor)
                            weekends[day] = weekend
                            current_weekend_doctor_index += 1
                            break
                    else:
                        print(f"⚠ No weekend doctor available on {day.isoformat()}")
                    continue
                elif day_name == "Sunday":
                    continue
                work_day = WorkingDay(day, day_name)
                available_doctors = []
                for doctor in doctors:
                    if doctor.is_available_on(day, day_name):
                        available_doctors.append(doctor)
                    else:
                        work_day.add_doctor_on_leave(doctor)

                num_doctors = len(available_doctors)
                doctor_counts.append(available_doctors)
                work_day.assign_available_doctors(available_doctors.copy())

                if num_doctors >= 6:
                    if num_doctors == 6:
                        day_duties = [1, 2, 3, 4, 5]
                    elif num_doctors == 7:
                        day_duties = [1,2,3,4,5,6]
                    else:
                        day_duties = [1,2,3,4,5,6,7]

                    duty_availability = {}

                    for duty in day_duties:
                        eligible_doctors = [doctor for doctor in available_doctors if duty in doctor.performable_duties]
                        eligible_doctors = [doctor for doctor in eligible_doctors if doctor.name != "N"]


                        duty_availability[duty] = eligible_doctors


                    work_day = assign_duties(work_day, duty_availability, dr_m, dr_p, dr_s)
                    working_days.append(work_day)

                else:
                    if num_doctors == 5:
                        day_duties = [1,2,3,4,5]

                        duty_availability = {}

                        for duty in day_duties:
                            eligible_doctors = [doctor for doctor in available_doctors if duty in doctor.performable_duties]
                            duty_availability[duty] = eligible_doctors

                        if 4 in duty_availability and dr_n in duty_availability[4]:
                            work_day.add_duties(dr_n, 4)
                            del duty_availability[4]

                        work_day = assign_duties(work_day, duty_availability, dr_m, dr_p, dr_s)
                        working_days.append(work_day)


                    else:
                        print("Less than 5 doctors available on this work day: " + work_day.date.strftime('%Y-%m-%d') + " Doctors: " + ", ".join(doctor.name for doctor in available_doctors))

    add_ef_to_workdays(working_days, weekends)

    return working_days, doctor_counts, weekends


def add_ef_to_workdays(working_days, weekends):
    ef_order = ["M", "P", "K", "Q", "S"] if date.today() < date(2025,12,1) else ["M", "P", "K", "Q", "S", "Z"]
    ef_index = 0

    weekly_days = defaultdict(list)
    for day in working_days:
        if not isinstance(day, Weekend):
            iso_week = day.date.isocalendar()[1]
            weekly_days[iso_week].append(day)

    for week, days in weekly_days.items():
        # Sort days Monday–Friday
        days.sort(key=lambda d: d.date.weekday())

        # Get weekend doctor for this week (Saturday)
        weekend_doctor = None
        for wknd_day, doc in weekends.items():
            if wknd_day.isocalendar()[1] == week:
                weekend_doctor = doc
                break

        # Identify EF-eligible doctors available this week
        ef_eligible_doctors = set()
        for day in days:
            for doctor in day.available_doctors:
                if doctor.name in ef_order:
                    ef_eligible_doctors.add(doctor.name)

        # CASE 1: Fewer than 6 EF-eligible doctors
        if len(ef_eligible_doctors) < 6:
            if weekend_doctor and weekend_doctor.doctor_assigned in ef_eligible_doctors:
                # Assign EF to weekend doctor on Tuesday if available
                tuesday = next((d for d in days if d.day_name == "Monday" and weekend_doctor in d.available_doctors),
                               None)
                if tuesday:
                    tuesday.ef_doctor = weekend_doctor
                    ef_eligible_doctors.remove(weekend_doctor.name)

        # CASE 2: 6 or more — weekend doctor should be excluded
        elif weekend_doctor and weekend_doctor.name in ef_eligible_doctors:
            ef_eligible_doctors.remove(weekend_doctor.name)

        # Assign EF from ef_order (only one per doctor per week)
        used_ef_doctors = set()
        for day in days:
            attempts = 0  # avoid infinite loop
            while attempts < len(ef_order):
                name = ef_order[ef_index % len(ef_order)]
                ef_index += 1
                attempts += 1

                # Skip the weekend doctor if it's Wed/Thu/Fri
                if day.day_name in ["Wednesday", "Thursday", "Friday"]:
                    if weekend_doctor and name == weekend_doctor.doctor_assigned.name:
                        continue

                if name in ef_eligible_doctors and name not in used_ef_doctors:
                    doctor = next((d for d in day.available_doctors if d.name == name), None)
                    if doctor:
                        day.doctor_on_ef = doctor
                        used_ef_doctors.add(name)
                        break

            if not day.doctor_on_ef:
                print(f"⚠ No EF doctor could be assigned on {day.date}")





