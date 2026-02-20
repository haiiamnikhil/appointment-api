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
