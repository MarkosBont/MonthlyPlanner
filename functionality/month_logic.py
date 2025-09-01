from functionality.doctor_roster import *
from functionality.working_day import WorkingDay
import calendar
from datetime import date

doctors = all_doctors()
working_days = []

weekend_order = ["P", "S", "M", "Q", "K", "Z"]
current_weekend = 3

duties = [1,2,3,4,5,6,7]
duty_availability = {}

today = date.today()

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
            work_day = WorkingDay(day, day_name)
            available_doctors = []
            for doctor in doctors:
                if doctor.is_available_on(day, day_name):
                    available_doctors.append(doctor)
                else:
                    work_day.add_doctor_on_leave(doctor)

            num_doctors = len(available_doctors)

            if num_doctors > 5:
                duty_availability = {}

                for duty in duties:
                    eligible_doctors = [doctor for doctor in available_doctors if duty in doctor.performable_duties]
                    if dr_n in eligible_doctors:
                        eligible_doctors.remove(dr_n)

                    duty_availability[duty] = eligible_doctors

                sorted_duties = sorted(duty_availability.items(), key=lambda x: len(x[1]))

                assigned_duties = {}
                used_doctors = set()

                for duty, candidates in sorted_duties:
                    candidates = [doctor for doctor in candidates if doctor not in used_doctors]

                    if not candidates:
                        assigned_duties[duty] = None
                        print(f"⚠ No doctor available for duty '{duty}' on {work_day.date}")
                        continue

                    selected = candidates[0]
                    assigned_duties[duty] = selected
                    used_doctors.add(selected)
                    work_day.add_duties(selected, duty)

            else:


        else:
            continue

