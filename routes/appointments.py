from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from config.database import SessionMaker
from schemas import request, response
from actions import appointments

router = APIRouter()


def get_db():
    db = SessionMaker()
    try:
        yield db
    finally:
        db.close()


@router.post('/ajax/v1/is-conflict/', response_model=List[response.AppointmentValidationResponse])
def validate_conflict_ajax(appointment: request.AppointmentValidationRequest, db: Session = Depends(get_db)):
    return appointments.AppointmentsActions.validate_conflict(db=db, request=appointment)


@router.post('/appointment/v1/create/', response_model=response.AppointmentCreateResponse)
def create_appointment_api(appointment: request.AppointmentRequest, db: Session = Depends(get_db)):
    return appointments.AppointmentsActions.create_appointment(db=db, request=appointment)


@router.get('/appointment/v1/list/', response_model=List[response.AppointmentCreateResponse])
def list_appointments_api(db: Session = Depends(get_db)):
    return appointments.AppointmentsActions.get_all_appointments(db=db)


@router.put('/appointment/v1/update/{appointment_id}', response_model=response.AppointmentCreateResponse)
def update_appointment_api(appointment_id: str, appointment: request.AppointmentUpdateRequest, db: Session = Depends(get_db)):
    return appointments.AppointmentsActions.update_appointment(db=db, appointment_id=appointment_id, request=appointment)


@router.delete('/appointment/v1/delete/{appointment_id}', response_model=response.AppointmentCreateResponse)
def delete_appointment_api(appointment_id: str, db: Session = Depends(get_db)):
    return appointments.AppointmentsActions.delete_appointment(db=db, appointment_id=appointment_id)


@router.patch('/appointment/v1/update/{appointment_id}', response_model=response.AppointmentCreateResponse)
def patch_appointment_api(appointment_id: str, appointment: request.AppointmentStatusUpdate, db: Session = Depends(get_db)):
    return appointments.AppointmentsActions.update_appointment(db=db, appointment_id=appointment_id, request=appointment)

