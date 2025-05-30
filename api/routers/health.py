"""
Health check endpoints for the Gugugu API
"""
from fastapi import APIRouter
from api.models.schemas import HealthResponse

router = APIRouter(
    prefix="/health",
    tags=["health"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=HealthResponse)
async def health_check():
    """
    Basic health check endpoint
    
    Returns:
        HealthResponse: Status of the API service
    """
    return HealthResponse(status="healthy")
