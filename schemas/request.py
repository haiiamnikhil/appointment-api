from pydantic import BaseModel
from datetime import datetime



from typing import List

class AppointmentRequest(BaseModel):
    title:str
    description:str
    start_time:datetime
    end_time:datetime
    participants: List[str] = []


