import uuid
from sqlalchemy.orm import Session
from models.appointment import Appointment
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

    @staticmethod
    def update_appointment(db: Session, appointment_id: str, appointment_request):
        database_appointment = AppointmentsData.get_appointment_by_id(db, appointment_id)
        if not database_appointment:
            return None
        
        if appointment_request.title is not None:
            database_appointment.title = appointment_request.title
        if appointment_request.description is not None:
            database_appointment.description = appointment_request.description
        if appointment_request.start_time is not None:
            database_appointment.start_time = appointment_request.start_time
        if appointment_request.end_time is not None:
            database_appointment.end_time = appointment_request.end_time
        if getattr(appointment_request, 'status', None) is not None:
            database_appointment.status = appointment_request.status
        
        # Replace participants only if strictly provided
        if appointment_request.participants is not None:
            db.query(Participants).filter(Participants.appointment_id == database_appointment.id).delete()
            database_appointment.participant = []
            for participant_name in appointment_request.participants:
                database_appointment.participant.append(
                    Participants(full_name=participant_name)
                )

        db.commit()
        db.refresh(database_appointment)
        return database_appointment

    @staticmethod
    def update_appointment_status(db: Session, appointment_id: str, status: str):
        database_appointment = AppointmentsData.get_appointment_by_id(db, appointment_id)
        if not database_appointment:
            return None
        
        database_appointment.status = status
        db.commit()
        db.refresh(database_appointment)
        return database_appointment
