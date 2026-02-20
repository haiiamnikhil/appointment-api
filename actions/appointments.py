from fastapi import HTTPException
from sqlalchemy.orm import Session

from data import appointments
from services import conflict_engine


class AppointmentsActions:

    @staticmethod
    def get_all_statuses():
        return {"statuses": [status.value for status in appointments.AppointmentsData.get_all_statuses()]}

    @staticmethod
    def get_appointments(db: Session):
        return appointments.AppointmentsData.get_all_appointments(db)

    @classmethod
    def get_appointment_by_id(cls, db: Session, appointment_id: str):
        database_appointment = appointments.AppointmentsData.get_appointment_by_id(db, appointment_id)
        if not database_appointment:
            raise HTTPException(status_code=404, detail="Appointment not found.")

        appointment_status = database_appointment.status.value if hasattr(database_appointment.status, 'value') else database_appointment.status

        return {
            "id": str(database_appointment.id),
            "title": database_appointment.title,
            "description": database_appointment.description,
            "start_time": database_appointment.start_time,
            "end_time": database_appointment.end_time,
            "status": appointment_status,
            "participants": [{"id": str(participant.id), "full_name": participant.full_name} for participant in database_appointment.participant]
        }

    @classmethod
    def validate_conflict(cls, db: Session, request):
        all_appointments = cls.get_appointments(db=db)
        conflicts = conflict_engine.get_conflicts_for_timeslot(request.start_time, request.end_time, all_appointments)
        
        response_list = []
        for appointment in conflicts:
            appointment_status = appointment.status.value if hasattr(appointment.status, 'value') else appointment.status
            response_list.append({
                "id": str(appointment.id),
                "title": appointment.title,
                "start_time": appointment.start_time,
                "end_time": appointment.end_time,
                "status": appointment_status,
                "is_conflict": True,
                "message": "Conflict found",
                "participants": [{"id": str(participant.id), "full_name": participant.full_name} for participant in appointment.participant]
            })
        return response_list

    @classmethod
    def create_appointment(cls, db: Session, request):
        all_appointments = cls.get_appointments(db=db)
        is_conflict = conflict_engine.check_conflict(request.start_time, request.end_time, all_appointments)

        if is_conflict:
            raise HTTPException(status_code=400, detail="Cannot create appointment. There is a scheduling conflict.")

        new_appointment = appointments.AppointmentsData.create_appointment(db, request)
        appointment_status = new_appointment.status.value if hasattr(new_appointment.status, 'value') else new_appointment.status

        return {
            "id": str(new_appointment.id),
            "title": new_appointment.title,
            "start_time": new_appointment.start_time,
            "end_time": new_appointment.end_time,
            "status": appointment_status,
            "participants": [{"id": str(participant.id), "full_name": participant.full_name} for participant in new_appointment.participant]
        }

    @classmethod
    def update_appointment(cls, db: Session, appointment_id: str, request):
        database_appointment = appointments.AppointmentsData.get_appointment_by_id(db, appointment_id)
        if not database_appointment:
            raise HTTPException(status_code=404, detail="Appointment not found.")

        request_start = getattr(request, 'start_time', None)
        request_end = getattr(request, 'end_time', None)
        
        effective_start_time = request_start if request_start is not None else database_appointment.start_time
        effective_end_time = request_end if request_end is not None else database_appointment.end_time

        all_appointments = cls.get_appointments(db=db)
        is_conflict = conflict_engine.check_conflict(effective_start_time, effective_end_time, all_appointments, exclude_id=appointment_id)
        
        if is_conflict:
            raise HTTPException(status_code=400, detail="Cannot update appointment. There is a scheduling conflict.")
            
        updated_appointment = appointments.AppointmentsData.update_appointment(db, appointment_id, request)
        if not updated_appointment:
            raise HTTPException(status_code=404, detail="Appointment not found.")
            
        appointment_status = updated_appointment.status.value if hasattr(updated_appointment.status, 'value') else updated_appointment.status
        
        return {
            "id": str(updated_appointment.id),
            "title": updated_appointment.title,
            "start_time": updated_appointment.start_time,
            "end_time": updated_appointment.end_time,
            "status": appointment_status,
            "participants": [{"id": str(participant.id), "full_name": participant.full_name} for participant in updated_appointment.participant]
        }

    @classmethod
    def delete_appointment(cls, db: Session, appointment_id: str):
        deleted_appointment = appointments.AppointmentsData.update_appointment_status(db, appointment_id, "Deleted")
        if not deleted_appointment:
            raise HTTPException(status_code=404, detail="Appointment not found.")
            
        appointment_status = deleted_appointment.status.value if hasattr(deleted_appointment.status, 'value') else deleted_appointment.status
        return {
            "id": str(deleted_appointment.id),
            "title": deleted_appointment.title,
            "start_time": deleted_appointment.start_time,
            "end_time": deleted_appointment.end_time,
            "status": appointment_status,
            "participants": [{"id": str(participant.id), "full_name": participant.full_name} for participant in deleted_appointment.participant]
        }



    @classmethod
    def get_all_appointments(cls, db: Session):
        query = cls.get_appointments(db=db)
        conflicts = conflict_engine.get_conflicting_appointment_ids(query)
        nearby_appointment_ids = conflict_engine.get_nearby_appointment_ids(query)

        response_list = []
        for appointment in query:
            is_conflict = appointment.id in conflicts
            is_nearby = appointment.id in nearby_appointment_ids

            appointment_status = appointment.status.value if hasattr(appointment.status, 'value') else appointment.status
            if appointment_status == "Scheduled" and is_nearby and not is_conflict:
                appointment_status = "Scheduled (Warning)"

            response_list.append({
                "id": str(appointment.id),
                "title": appointment.title,
                "start_time": appointment.start_time,
                "end_time": appointment.end_time,
                "status": appointment_status,
                "participants": [{"id": str(participant.id), "full_name": participant.full_name} for participant in appointment.participant]
            })
        return response_list
