# Appointment API Microservice

A Python-based backend microservice built with **FastAPI** and **SQLAlchemy** to manage and schedule appointments.

This API provides endpoints for scheduling meetings, validating participants, and an integrated **Conflict Detection Engine** that strictly blocks overlapping time slots automatically while monitoring for adjacent schedules to throw warnings.

---

## 🚀 Features

- **FastAPI Framework:** High-performance async routing with built-in OpenAPI/Swagger docs.
- **Conflict Prevention Engine:** Ensures no two appointments occupy the exact same timeline.
- **Smart Warnings System:** Automatically flags appointments as `Scheduled (Warning)` if another meeting is scheduled sequentially (within 30 minutes).
- **Participant Mapping:** Supports scheduling multiple dynamic participants per meeting.
- **Enum Status Tracking:** Tracks appointment life cycles: `In-progress`, `Canceled`, `Scheduled`, and `Deleted`.

---

## 🛠️ Tech Stack

- **Backend:** Python + FastAPI
- **Database:** SQLite (via SQLAlchemy ORM)
- **Validation:** Pydantic (V2)
- **ASGI Server:** Uvicorn

---

## 📦 Installation & Setup

1. **Clone the repository** (if you haven't already):

```bash
git clone https://github.com/haiiamnikhil/appointment-api.git
cd appointment-api/api
```

2. **Create a Virtual Environment** (Recommended):

```bash
python -m venv .venv
# Activate on Windows:
.\.venv\Scripts\activate
# Activate on Linux/Mac:
source .venv/bin/activate
```

3. **Install Dependencies**:

```bash
pip install "fastapi[all]" sqlalchemy
```

4. **Initialize Database & Run Server**:

```bash
uvicorn main:app --reload
```

---

## 📡 API Endpoints

Once running, navigate to the auto-generated Swagger documentation at `http://127.0.0.1:8000/docs` to test!

### 1. `POST /appointment/v1/create/`

Creates a new appointment.
**Payload:**

```json
{
  "title": "Strategy Sync",
  "description": "Discussing architectural changes",
  "start_time": "2026-02-21T10:00:00Z",
  "end_time": "2026-02-21T11:00:00Z",
  "participants": ["Alice", "Bob"]
}
```

**Response (Success):** returns the dictionary mapped with a dynamically assigned ID and status string. Raises a `400 Bad Request` if the target timeslot is already booked.

### 2. `GET /appointment/v1/list/`

Retrieves all scheduled appointments securely ordered chronologically while injecting `Scheduled (Warning)` status properties if back-to-back meeting buffers are triggered.

### 3. `POST /ajax/v1/is-conflict/`

Validates whether a proposed timeframe overlaps against the database silently mapping an `is_conflict` boolean string to the client.

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the issues page.
