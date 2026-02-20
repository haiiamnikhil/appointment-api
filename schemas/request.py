from pydantic import BaseModel
from datetime import datetime



from typing import List, Optional

class AppointmentValidationRequest(BaseModel):
    start_time: datetime
    end_time: datetime

class AppointmentRequest(BaseModel):
    title: str
    description: Optional[str] = None
    start_time: datetime
    end_time: datetime
    participants: List[str] = []

class AppointmentUpdateRequest(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    participants: Optional[List[str]] = None

class AppointmentStatusUpdate(BaseModel):
    status: str
