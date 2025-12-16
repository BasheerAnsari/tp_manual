from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError

from core_services.app.routes.recruiter_routes import router as recruiter_router
from core_services.app.routes.dashboard_routes import router as dashboard_router
from core_services.app.routes.department_routes import router as department_router
from core_services.app.core.database import Base, engine
from core_services.app.models.recruiter_model import Recruiter
from core_services.app.routes.job_router import job_router
from core_services.app.config import get_settings
from core_services.app.shared.helper.validation_handler import validation_exception_handler


settings = get_settings()

app = FastAPI(title="TalentPool365 Recruiter Service")

app.add_exception_handler(
    RequestValidationError,
    validation_exception_handler
)

# Create DB Tables
Base.metadata.create_all(bind=engine)

# Register & ignin Routes
app.include_router(recruiter_router)

# job addition / job routs 
app.include_router(job_router)

# recruiter dashbord 
app.include_router(dashboard_router)

# departments
app.include_router(department_router)


# Middware  
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

@app.get("/")
def root():
    return {
        "status": "Recruiter Service Running Successfully",
        "environment": settings.ENVIRONMENT
    }
