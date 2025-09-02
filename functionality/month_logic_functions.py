def assign_duties(
    work_day,
    duty_availability,
    dr_m,
    dr_p,
    dr_s):

    assigned_duties = {}
    used_doctors = set()

    # Manual assignments
    if work_day.day_name in ["Thursday", "Friday"]:
        if 5 in duty_availability and dr_m in duty_availability[5]:
            assigned_duties[5] = dr_m
            used_doctors.add(dr_m)
            work_day.add_duties(dr_m, 5)
            del duty_availability[5]

    if work_day.day_name == "Monday":
        if 5 in duty_availability and dr_p in duty_availability[5]:
            assigned_duties[5] = dr_p
            used_doctors.add(dr_p)
            work_day.add_duties(dr_p, 5)
            del duty_availability[5]

    # Sort duties after manual assignments
    sorted_duties = sorted(duty_availability.items(), key=lambda x: len(x[1]))

    for duty, candidates in sorted_duties:
        if duty in assigned_duties:
            continue

        candidates = [
            doctor for doctor in candidates
            if doctor not in used_doctors
            and not (
                doctor == dr_s
                and duty in [5, 6, 7]
                and work_day.day_name != "Wednesday"
            )
        ]

        if not candidates:
            assigned_duties[duty] = None
            print(f"⚠ No doctor available for duty '{duty}' on {work_day.date.strftime('%Y-%m-%d')}")
            continue

        selected = candidates[0]
        assigned_duties[duty] = selected
        used_doctors.add(selected)
        work_day.add_duties(selected, duty)

    return work_day