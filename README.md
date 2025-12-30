# TP365 Job Service

TP365 Job Service is a backend microservice responsible for managing recruiter authentication, job postings, and related workflows.  
It is designed with scalability, clean architecture, and standardized API responses in mind.

---

## 🚀 Tech Stack

- **Python 3.10+**
- **FastAPI**
- **SQLAlchemy**
- **PostgreSQL**
- **JWT Authentication**
- **Pydantic**
- **Uvicorn**

---

## 🧩 Key Features

- Recruiter signup and signin
- JWT-based authentication (access & refresh tokens)
- Job creation, update, listing, and filtering
- Pagination support for listing APIs
- Standardized API response structure
- Centralized error logging
- Modular service-based architecture

---

## 📂 Project Structure

core_services/
├── app/
│ ├── core/ # App configs & startup
│ ├── models/ # SQLAlchemy models
│ ├── schemas/ # Pydantic schemas
│ ├── routes/ # API routes
│ ├── services/ # Business logic
│ ├── shared/ # Common helpers (pagination, responses, logging)
│ └── main.py # FastAPI entry point
├── logs/ # Error & application logs
└── requirements.txt

---

# install the requirements
pip install -r requirements.txt

# Running the Application
python -m uvicorn core_services.app.main:app --reload

Application will be available at:http://127.0.0.1:8000

API Documentation : http://127.0.0.1:8000/docs

Status
