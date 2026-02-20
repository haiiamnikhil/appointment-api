import uuid
from sqlalchemy.orm import Session
from models.appointment import Appointment
from models.participants import Participants

class AppointmentsData:

    @staticmethod
    def get_all_appointments(db: Session):
        return db.query(Appointment).order_by(Appointment.start_time.asc()).all()

    @staticmethod
    def create_appointment(db: Session, request):
        db_appointment = Appointment(
            title=request.title,
            description=request.description,
            start_time=request.start_time,
            end_time=request.end_time,
            status=request.status if hasattr(request, "status") and request.status else "Scheduled"
        )
        
        for p_name in request.participants:
            db_appointment.participant.append(
                Participants(full_name=p_name)
            )

        db.add(db_appointment)
        db.commit()
        db.refresh(db_appointment)
        return db_appointment

    @staticmethod
    def get_appointment_by_id(db: Session, appointment_id: str):
        try:
            uid = uuid.UUID(appointment_id)
        except ValueError:
            return None
        return db.query(Appointment).filter(Appointment.id == uid).first()

    @staticmethod
    def update_appointment(db: Session, appointment_id: str, request):
        db_appointment = AppointmentsData.get_appointment_by_id(db, appointment_id)
        if not db_appointment:
            return None
        
        db_appointment.title = request.title
        db_appointment.description = request.description
        db_appointment.start_time = request.start_time
        db_appointment.end_time = request.end_time
        
        # Replace participants
        db.query(Participants).filter(Participants.appointment_id == db_appointment.id).delete()
        db_appointment.participant = []
        for p_name in request.participants:
            db_appointment.participant.append(
                Participants(full_name=p_name)
            )

        db.commit()
        db.refresh(db_appointment)
        return db_appointment

    @staticmethod
    def update_appointment_status(db: Session, appointment_id: str, status: str):
        db_appointment = AppointmentsData.get_appointment_by_id(db, appointment_id)
        if not db_appointment:
            return None
        
        db_appointment.status = status
        db.commit()
        db.refresh(db_appointment)
        return db_appointment
