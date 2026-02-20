# Manage Appointments Microservice API

A robust FastAPI backend microservice for scheduling, validating, and managing dynamic appointments. It uses SQLAlchemy for robust ORM data handling and Pydantic for rigid, granular input/output schema validation.

## Core Features

- **Conflict Engine**: Automatically prevents double-booking across participants via an active time-boundary collision algorithm (`services/conflict_engine.py`).
- **Granular API Schemas**: Tightly decoupled schemas ensuring explicit validation boundaries (e.g., separating creation requirements from status patches).
- **Dynamic Status Updates**: Lightweight integration using strict `enum` types (`scheduled`, `in-progress`, `canceled`, `completed`, `deleted`).
- **Soft Deletion**: Records can be dynamically archived or canceled without permanently dropping rows from the underlying database relationships.

---

## Application Architecture

The application is structured into decoupled layers allowing clean business logic interpolation:

- **`routes/appointments.py`**: API controllers defining FastAPI routes and injecting `Session` dependencies.
- **`actions/appointments.py`**: Intermediary logic evaluating conflict structures and manipulating outputs before Database injection.
- **`data/appointments.py`**: Core SQLAlchemy operations reading and mutating explicit records.
- **`models/`**: SQL relational tables mapping Python object attributes natively onto persistent Data architectures.
- **`schemas/`**: Pydantic validation structures rigidly matching inbound (`requests.py`) and outbound (`responses.py`) endpoints securely.

---

## API Endpoints (`/appointment/v1/`)

### 1. `POST /create/`

Create a brand new appointment manually. By default, applications successfully built through here will internally map to `status: "scheduled"`.
**Request Payload Layout (`AppointmentRequest`)**:

```json
{
  "title": "Strategy Sync",
  "description": "Quarterly planning.",
  "start_time": "2024-03-25T10:00:00Z",
  "end_time": "2024-03-25T11:00:00Z",
  "participants": ["John Doe", "Jane Smith"]
}
```

### 2. `POST /ajax/v1/is-conflict/`

Validates an incoming timeframe strictly to assert if _any_ scheduling boundary logic exists across the entire database. Excludes canceled or deleted relationships seamlessly.
**Request Payload Layout (`AppointmentValidationRequest`)**:

```json
{
  "start_time": "2024-03-25T10:00:00Z",
  "end_time": "2024-03-25T11:00:00Z"
}
```

**Response Details**: Distinctively returns an `AppointmentValidationResponse` array dynamically injecting `"is_conflict": true` on colliding events cleanly.

### 3. `GET /list/`

Retrieves a Chronologically ordered array of every appointment mapped into the backend natively.

### 4. `PUT /update/{appointment_id}`

Overwrites standard editable inputs safely. Explicitly supports partial-patch mapping dynamically via Pydantics `Optional[...]` parameters.
**Request Payload Layout (`AppointmentUpdateRequest`)**:

```json
{
  "title": "Strategy Sync Updated",
  "start_time": "2024-03-25T11:30:00Z",
  "participants": ["John Doe"]
}
```

### 5. `PATCH /update/{appointment_id}`

Dynamically manipulates strictly the database `status` indexing safely preventing overlapping payloads updating broader requirements improperly.
**Request Payload Layout (`AppointmentStatusUpdate`)**:

```json
{
  "status": "completed"
}
```

### 6. `DELETE /delete/{appointment_id}`

Performs intuitive "Soft Deletions" targeting the ID and permanently appending the `"deleted"` string directly toward the database index cleanly.

---

## Development & Setup

### Requirements

- **Python 3.10+**
- **FastAPI**
- **SQLAlchemy** (Native SQLite bindings mapped inherently via `Base.metadata.create_all(bind=engine)`)

### Quick Start

```bash
# Optional Setup: Create Virtual Environment
python -m venv venv
source venv/bin/activate  # (Windows: venv\Scripts\activate)

# 1. Install Dependencies
pip install -r requirements.txt

# 2. Boot Application
python main.py
```

- **Interactive API Documentation (Swagger)**: http://127.0.0.1:8000/docs
- **Alternative Redoc**: http://127.0.0.1:8000/redoc
