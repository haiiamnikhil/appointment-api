from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config.database import engine, Base
from routes import appointments
import uvicorn
from models.appointment import Appointment
from models.participants import Participants

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Manage appointments microservice api")

app.include_router(router=appointments.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )
