import uuid
import enum
from sqlalchemy import Column, String, DateTime, Uuid, Text, Enum
from sqlalchemy.orm import relationship
from config.database import Base


class AppointmentStatus(str, enum.Enum):
    in_progress = "in-progress"
    canceled = "canceled"
    scheduled = "scheduled"
    deleted = "deleted"
    completed = "completed"

class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4, index=True)
    title = Column(String, unique=False, nullable=False, default="Un-named Title")
    description = Column(Text, unique=False, nullable=True)
    start_time = Column(DateTime, nullable=False, index=True)
    end_time = Column(DateTime, nullable=False, index=True)
    status = Column(Enum(AppointmentStatus), default=AppointmentStatus.scheduled, nullable=False)

    participant = relationship("Participants", back_populates="appointment", cascade="all, delete-orphan")
