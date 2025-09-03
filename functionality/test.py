from functionality.classes.doctor import Doctor
from datetime import date
from month_logic import *

dr_n = Doctor(name="N",
              performable_duties=[4], # only if there are 5 doctors (not more)
              working_days=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
              working_wknd=False,
              num_ef=0
              )

dr_i = Doctor(name="I",
              performable_duties=[1,3,7],
              working_days=["Tuesday", "Friday"],
              working_wknd=False,
              num_ef=2, # per month
              dates_of_leave=[(date(2025, 10, 22), date(2025, 10, 25))])

dr_g = Doctor(name="G",
              performable_duties=[1,3,7],
              working_days=["Tuesday"],
              working_wknd=False,
              num_ef=1 # per month
              )

dr_y = Doctor(name="Y",
              performable_duties=[1,3,7],
              working_days=["Monday"],
              working_wknd=False,
              num_ef=1 # per month
              )

dr_z = Doctor(name="Z",
              performable_duties=[1,3,5,6,7] if date.today() >= date(2025, 12, 1) else [1,3,6,7] if date.today() >= date(2025, 11, 1) else [], # After 1/12/25, he will be able to also do duty 5
              working_days=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"] if date.today() >= date(2025,11,1) else [], # Only after 1/11/25
              working_wknd=True # Only from after 1/12/2025
              )

dr_s = Doctor(name="S",
              performable_duties=[1,3,5,6,7],
              working_days=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
              working_wknd=True
              )

dr_q = Doctor(name="Q",
              performable_duties=[1,2,3,4,5,6,7],
              working_days=["Monday", "Wednesday", "Thursday", "Friday"] if date.today() < date(2026, 1, 1) else ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], # Doesn't work on Tuesdays until 31/12/2025
              working_wknd=True,
              dates_of_leave=[(date(2025, 10, 15), date(2025, 10, 20))])

dr_k = Doctor(name="K",
              performable_duties=[1,2,3,4,5,6],
              working_days=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
              working_wknd=True)

dr_m = Doctor(name="M",
              performable_duties=[1,2,3,4,5],
              working_days=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
              working_wknd=True,
              dates_of_leave=[(date(2025, 10, 5), date(2025, 10, 11))])

dr_p = Doctor(name="P",
              performable_duties=[1,2,4,5,6],
              working_days=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
              working_wknd=True)

doctors = [dr_p,dr_m,dr_k, dr_q, dr_s, dr_z, dr_y, dr_g, dr_i, dr_n]

working_days, doctor_counts = generate_working_days(doctors)


for i in range(len(doctor_counts)):
    day = working_days[i]
    if isinstance(day, Weekend):
        print("WEEKEND: Dr " + day.doctor_assigned.name + "\n")
        continue
    number_of_doctors = doctor_counts[i]
    print("Date: " + day.date.strftime('%Y-%m-%d') + " \nDuties assigned: \n" + day.return_duties() + "Number of doctors: " + str(number_of_doctors) + "\n")


