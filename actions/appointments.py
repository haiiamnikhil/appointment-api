from sqlalchemy.orm import Session
from data import appointments
from services import conflict_engine

from fastapi import HTTPException


class AppointmentsActions:

    @staticmethod
    def get_appointments(db: Session):
        return appointments.AppointmentsData.get_all_appointments(db)

    @classmethod
    def validate_conflict(cls, db: Session, request):
        all_appointments = cls.get_appointments(db=db)
        is_conflict = conflict_engine.check_conflict(request.start_time, request.end_time, all_appointments)
        return {
            "id": "",
            "title": request.title,
            "start_time": request.start_time,
            "end_time": request.end_time,
            "status": "Scheduled",
            "is_conflict": is_conflict,
            "message": "Conflict found" if is_conflict else "No conflict",
            "participant": []
        }

    @classmethod
    def create_appointment(cls, db: Session, request):
        all_apts = cls.get_appointments(db=db)
        is_conflict = conflict_engine.check_conflict(request.start_time, request.end_time, all_apts)

        if is_conflict:
            raise HTTPException(status_code=400, detail="Cannot create appointment. There is a scheduling conflict.")

        new_apt = appointments.AppointmentsData.create_appointment(db, request)
        status_str = new_apt.status.value if hasattr(new_apt.status, 'value') else new_apt.status

        return {
            "id": str(new_apt.id),
            "title": new_apt.title,
            "start_time": new_apt.start_time,
            "end_time": new_apt.end_time,
            "status": status_str,
            "is_conflict": is_conflict,
            "message": "Appointment created with conflict" if is_conflict else "Appointment created successfully",
            "participant": [{"id": str(p.id), "full_name": p.full_name} for p in new_apt.participant]
        }

    @classmethod
    def get_all_appointments(cls, db: Session):
        query = cls.get_appointments(db=db)
        conflicts = conflict_engine.get_conflicting_appointment_ids(query)
        nearbys = conflict_engine.get_nearby_appointment_ids(query)

        response_list = []
        for apt in query:
            is_conflict = apt.id in conflicts
            is_nearby = apt.id in nearbys

            status_str = apt.status.value if hasattr(apt.status, 'value') else apt.status
            if status_str == "Scheduled" and is_nearby and not is_conflict:
                status_str = "Scheduled (Warning)"

            response_list.append({
                "id": str(apt.id),
                "title": apt.title,
                "start_time": apt.start_time,
                "end_time": apt.end_time,
                "status": status_str,
                "is_conflict": is_conflict,
                "message": "Conflict found" if is_conflict else "No conflict",
                "participant": [{"id": str(p.id), "full_name": p.full_name} for p in apt.participant]
            })
        return response_list
