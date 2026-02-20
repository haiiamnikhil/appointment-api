import uuid

from sqlalchemy import Column, Uuid, String, ForeignKey
from sqlalchemy.orm import relationship
from config.database import Base


class Participants(Base):
    __tablename__ = "participants"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    appointment_id = Column(Uuid, ForeignKey('appointments.id', ondelete='CASCADE'))
    full_name = Column(String, unique=False)

    appointment = relationship("Appointment", back_populates="participant")
