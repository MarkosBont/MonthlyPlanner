from functionality.doctor_roster import *
from functionality.classes.working_day import WorkingDay
import calendar
from datetime import date
from month_logic_functions import assign_duties

def generate_working_days(doctors):
    working_days = []
    doctor_counts = []

    weekend_order = ["P", "S", "M", "Q", "K", "Z"]
    current_weekend = 3

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
                    doctor_counts.append(num_doctors)
                    if num_doctors == 6:
                        day_duties = [1, 2, 3, 4, 5]
                    elif num_doctors == 7:
                        day_duties = [1,2,3,4,5,6]
                    else:
                        day_duties = [1,2,3,4,5,6,7]

                    duty_availability = {}

                    for duty in day_duties:
                        eligible_doctors = [doctor for doctor in available_doctors if duty in doctor.performable_duties]
                        if dr_n in eligible_doctors:
                            eligible_doctors.remove(dr_n)

                        duty_availability[duty] = eligible_doctors

                    work_day = assign_duties(work_day, duty_availability, dr_m, dr_p, dr_s)
                    working_days.append(work_day)

                else:
                    if num_doctors == 5:
                        doctor_counts.append(num_doctors)
                        day_duties = [1,2,3,4,5]

                        duty_availability = {}

                        for duty in day_duties:
                            eligible_doctors = [doctor for doctor in available_doctors if duty in doctor.performable_duties]
                            duty_availability[duty] = eligible_doctors

                        work_day = assign_duties(work_day, duty_availability, dr_m, dr_p, dr_s)
                        working_days.append(work_day)


                    else:
                        print("Less than 5 doctors available on this work day: " + work_day.date.strftime('%Y-%m-%d'))

    return working_days, doctor_counts