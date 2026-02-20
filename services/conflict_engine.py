def make_naive(dt):
    if dt.tzinfo is not None:
        return dt.replace(tzinfo=None)
    return dt

def check_conflict(new_start, new_end, existing_appointments):
    ns = make_naive(new_start)
    ne = make_naive(new_end)
    for apt in existing_appointments:
        a_s = make_naive(apt.start_time)
        a_e = make_naive(apt.end_time)
        # Using <= and >= to catch exact same start and end times
        if ns < a_e and ne > a_s:
            return True
        elif ns == a_s and ne == a_e:
            return True
    return False

from datetime import timedelta

def get_conflicting_appointment_ids(appointments):
    conflicts = set()
    for i in range(len(appointments)):
        for j in range(i + 1, len(appointments)):
            start_i = make_naive(appointments[i].start_time)
            end_i = make_naive(appointments[i].end_time)
            start_j = make_naive(appointments[j].start_time)
            end_j = make_naive(appointments[j].end_time)
            if start_i < end_j and end_i > start_j:
                conflicts.add(appointments[i].id)
                conflicts.add(appointments[j].id)
            elif start_i == start_j and end_i == end_j:
                conflicts.add(appointments[i].id)
                conflicts.add(appointments[j].id)

    return conflicts

def get_nearby_appointment_ids(appointments, buffer_minutes=30):
    nearbys = set()
    for i in range(len(appointments)):
        for j in range(i + 1, len(appointments)):
            start_i = make_naive(appointments[i].start_time)
            end_i = make_naive(appointments[i].end_time)
            start_j = make_naive(appointments[j].start_time)
            end_j = make_naive(appointments[j].end_time)
            
            # Check if j starts within buffer of i ending, or i starts within buffer of j ending
            if (end_i <= start_j <= end_i + timedelta(minutes=buffer_minutes)) or \
               (end_j <= start_i <= end_j + timedelta(minutes=buffer_minutes)):
                nearbys.add(appointments[i].id)
                nearbys.add(appointments[j].id)
    return nearbys
