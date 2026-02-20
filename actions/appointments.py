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
    def update_appointment(cls, db: Session, appointment_id: str, request):
        all_apts = cls.get_appointments(db=db)
        is_conflict = conflict_engine.check_conflict(request.start_time, request.end_time, all_apts, exclude_id=appointment_id)
        
        if is_conflict:
            raise HTTPException(status_code=400, detail="Cannot update appointment. There is a scheduling conflict.")
            
        updated_apt = appointments.AppointmentsData.update_appointment(db, appointment_id, request)
        if not updated_apt:
            raise HTTPException(status_code=404, detail="Appointment not found.")
            
        status_str = updated_apt.status.value if hasattr(updated_apt.status, 'value') else updated_apt.status
        
        return {
            "id": str(updated_apt.id),
            "title": updated_apt.title,
            "start_time": updated_apt.start_time,
            "end_time": updated_apt.end_time,
            "status": status_str,
            "is_conflict": is_conflict,
            "message": "Appointment updated successfully",
            "participant": [{"id": str(p.id), "full_name": p.full_name} for p in updated_apt.participant]
        }

    @classmethod
    def delete_appointment(cls, db: Session, appointment_id: str):
        deleted_apt = appointments.AppointmentsData.update_appointment_status(db, appointment_id, "Deleted")
        if not deleted_apt:
            raise HTTPException(status_code=404, detail="Appointment not found.")
        return {"message": "Appointment deleted successfully"}

    @classmethod
    def cancel_appointment(cls, db: Session, appointment_id: str):
        canceled_apt = appointments.AppointmentsData.update_appointment_status(db, appointment_id, "Canceled")
        if not canceled_apt:
            raise HTTPException(status_code=404, detail="Appointment not found.")
        return {"message": "Appointment canceled successfully"}

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
