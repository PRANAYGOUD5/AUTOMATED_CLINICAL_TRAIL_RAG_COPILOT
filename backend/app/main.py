"""
FastAPI application entry point.
This is the module Uvicorn imports and runs — the ASGI server
looks for a variable named `app` here by convention.
"""

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(
    title="Clinical Trial & Medical Imaging RAG Copilot",
    description="Backend API for scan analysis, protocol RAG, and eligibility agents",
    version="0.1.0",
)


class HealthResponse(BaseModel):
    status: str
    service: str


@app.get("/", tags=["root"])
async def root():
    """Simple landing route — confirms the API is reachable."""
    return {"message": "Clinical Trial RAG Copilot API is running"}


@app.get("/health", response_model=HealthResponse, tags=["monitoring"])
async def health_check():
    """
    Health check endpoint.
    Real companies use this for uptime monitoring and load balancer
    checks — if this returns anything other than 200 OK, the
    service is considered down.
    """
    return HealthResponse(status="ok", service="clinical-rag-copilot-backend")
