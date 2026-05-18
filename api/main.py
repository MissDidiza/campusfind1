"""
main.py — FastAPI Application Entry Point
==========================================
Wires all routers together and configures the application.

To run locally:
    pip install fastapi uvicorn pydantic
    uvicorn api.main:app --reload

Swagger UI:  http://localhost:8000/docs
ReDoc:       http://localhost:8000/redoc
OpenAPI JSON: http://localhost:8000/openapi.json
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routers import users, reports, matches

app = FastAPI(
    title="CampusFind API",
    description=(
        "REST API for the CampusFind Smart Campus Lost & Found System. "
        "Supports user registration, lost/found report submission, "
        "and AI-powered match management."
    ),
    version="1.0.0",
    contact={
        "name": "CampusFind Development",
        "email": "dev@university.ac.za",
    },
    license_info={
        "name": "MIT",
    },
)

# CORS — allow frontend to call the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(users.router)
app.include_router(reports.router)
app.include_router(matches.router)


@app.get("/", tags=["Health"])
def root():
    """Health check endpoint."""
    return {
        "system": "CampusFind API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs",
    }


@app.get("/health", tags=["Health"])
def health():
    return {"status": "healthy"}
