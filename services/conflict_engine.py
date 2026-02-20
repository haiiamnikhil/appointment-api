def make_naive(dt):
    if dt.tzinfo is not None:
        return dt.replace(tzinfo=None)
    return dt

def check_conflict(new_start, new_end, existing_appointments, exclude_id=None):
    naive_new_start = make_naive(new_start)
    naive_new_end = make_naive(new_end)
    for appointment in existing_appointments:
        appointment_status = appointment.status.value if hasattr(appointment.status, 'value') else appointment.status
        if appointment_status in ["canceled", "deleted"]:
            continue
        if exclude_id and str(appointment.id) == str(exclude_id):
            continue
        
        naive_existing_start = make_naive(appointment.start_time)
        naive_existing_end = make_naive(appointment.end_time)
        # Using <= and >= to catch exact same start and end times
        if naive_new_start < naive_existing_end and naive_new_end > naive_existing_start:
            return True
        elif naive_new_start == naive_existing_start and naive_new_end == naive_existing_end:
            return True
    return False

def get_conflicts_for_timeslot(new_start, new_end, existing_appointments, exclude_id=None):
    conflicting_appointments = []
    naive_new_start = make_naive(new_start)
    naive_new_end = make_naive(new_end)
    for appointment in existing_appointments:
        appointment_status = appointment.status.value if hasattr(appointment.status, 'value') else appointment.status
        if appointment_status in ["canceled", "deleted"]:
            continue
        if exclude_id and str(appointment.id) == str(exclude_id):
            continue
        
        naive_existing_start = make_naive(appointment.start_time)
        naive_existing_end = make_naive(appointment.end_time)
        
        if naive_new_start < naive_existing_end and naive_new_end > naive_existing_start:
            conflicting_appointments.append(appointment)
        elif naive_new_start == naive_existing_start and naive_new_end == naive_existing_end:
            conflicting_appointments.append(appointment)
    return conflicting_appointments

from datetime import timedelta

def get_conflicting_appointment_ids(appointments):
    conflict_ids = set()
    for i in range(len(appointments)):
        status_i = appointments[i].status.value if hasattr(appointments[i].status, 'value') else appointments[i].status
        if status_i in ["canceled", "deleted"]:
            continue
            
        for j in range(i + 1, len(appointments)):
            status_j = appointments[j].status.value if hasattr(appointments[j].status, 'value') else appointments[j].status
            if status_j in ["canceled", "deleted"]:
                continue
                
            start_i = make_naive(appointments[i].start_time)
            end_i = make_naive(appointments[i].end_time)
            start_j = make_naive(appointments[j].start_time)
            end_j = make_naive(appointments[j].end_time)
            if start_i < end_j and end_i > start_j:
                conflict_ids.add(appointments[i].id)
                conflict_ids.add(appointments[j].id)
            elif start_i == start_j and end_i == end_j:
                conflict_ids.add(appointments[i].id)
                conflict_ids.add(appointments[j].id)

    return conflict_ids

def get_nearby_appointment_ids(appointments, buffer_minutes=30):
    nearby_ids = set()
    for i in range(len(appointments)):
        status_i = appointments[i].status.value if hasattr(appointments[i].status, 'value') else appointments[i].status
        if status_i in ["canceled", "deleted"]:
            continue
            
        for j in range(i + 1, len(appointments)):
            status_j = appointments[j].status.value if hasattr(appointments[j].status, 'value') else appointments[j].status
            if status_j in ["canceled", "deleted"]:
                continue
                
            start_i = make_naive(appointments[i].start_time)
            end_i = make_naive(appointments[i].end_time)
            start_j = make_naive(appointments[j].start_time)
            end_j = make_naive(appointments[j].end_time)
            
            # Check if j starts within buffer of i ending, or i starts within buffer of j ending
            if (end_i <= start_j <= end_i + timedelta(minutes=buffer_minutes)) or \
               (end_j <= start_i <= end_j + timedelta(minutes=buffer_minutes)):
                nearby_ids.add(appointments[i].id)
                nearby_ids.add(appointments[j].id)
    return nearby_ids
