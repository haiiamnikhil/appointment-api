from pydantic import BaseModel
from datetime import datetime
from typing import List
from models.appointment import AppointmentStatus

class ParticipantResponse(BaseModel):
    id: str
    full_name: str

    class Config:
        from_attributes = True


class AppointmentCreateResponse(BaseModel):
    id: str
    title: str
    start_time: datetime
    end_time: datetime
    status: AppointmentStatus
    is_conflict: bool
    message: str
    participant: List[ParticipantResponse] = []

    class Config:
        from_attributes = True

