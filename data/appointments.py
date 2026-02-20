import uuid
from sqlalchemy.orm import Session
from models.appointment import Appointment, AppointmentStatus
from models.participants import Participants

class AppointmentsData:

    @staticmethod
    def get_all_appointments(db: Session):
        return db.query(Appointment).order_by(Appointment.start_time.asc()).all()

    @staticmethod
    def create_appointment(db: Session, appointment_request):
        database_appointment = Appointment(
            title=appointment_request.title,
            description=appointment_request.description,
            start_time=appointment_request.start_time,
            end_time=appointment_request.end_time,
            status="scheduled"
        )
        
        for participant_name in appointment_request.participants:
            database_appointment.participant.append(
                Participants(full_name=participant_name)
            )

        db.add(database_appointment)
        db.commit()
        db.refresh(database_appointment)
        return database_appointment

    @staticmethod
    def get_appointment_by_id(db: Session, appointment_id: str):
        try:
            appointment_uuid = uuid.UUID(appointment_id)
        except ValueError:
            return None
        return db.query(Appointment).filter(Appointment.id == appointment_uuid).first()

    @classmethod
    def update_appointment(cls, db: Session, appointment_id: str, appointment_request):
        database_appointment = cls.get_appointment_by_id(db, appointment_id)
        if not database_appointment:
            return None
        
        req_title = getattr(appointment_request, 'title', None)
        req_description = getattr(appointment_request, 'description', None)
        req_start_time = getattr(appointment_request, 'start_time', None)
        req_end_time = getattr(appointment_request, 'end_time', None)
        req_status = getattr(appointment_request, 'status', None)
        req_participants = getattr(appointment_request, 'participants', None)

        if req_title is not None:
            database_appointment.title = req_title
        if req_description is not None:
            database_appointment.description = req_description
        if req_start_time is not None:
            database_appointment.start_time = req_start_time
        if req_end_time is not None:
            database_appointment.end_time = req_end_time
        if req_status is not None:
            database_appointment.status = req_status
        
        # Replace participants only if strictly provided
        if req_participants is not None:
            db.query(Participants).filter(Participants.appointment_id == database_appointment.id).delete()
            database_appointment.participant = []
            for participant_name in req_participants:
                database_appointment.participant.append(
                    Participants(full_name=participant_name)
                )

        db.commit()
        db.refresh(database_appointment)
        return database_appointment

    @classmethod
    def update_appointment_status(cls, db: Session, appointment_id: str, status: str):
        database_appointment = cls.get_appointment_by_id(db, appointment_id)
        if not database_appointment:
            return None
        
        database_appointment.status = status
        db.commit()
        db.refresh(database_appointment)
        return database_appointment

    @staticmethod
    def get_all_statuses():
        return AppointmentStatus
