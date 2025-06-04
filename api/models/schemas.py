"""
Pydantic models for the Gugugu API
"""
from pydantic import BaseModel
from typing import List, Optional


class AIRequest(BaseModel):
    """Request model for AI chat endpoints"""
    message: str
    max_tokens: Optional[int] = 1000
    temperature: Optional[float] = 0.7


class AIStreamRequest(BaseModel):
    """Request model for AI streaming chat endpoints"""
    message: str
    max_tokens: Optional[int] = 1000
    temperature: Optional[float] = 0.7


class AIResponse(BaseModel):
    """Response model for AI chat endpoints"""
    response: str
    model: str
    usage: Optional[dict] = None


class HealthResponse(BaseModel):
    """Health check response model"""
    status: str


class AIHealthResponse(BaseModel):
    """AI health check response model"""
    status: str
    model: Optional[str] = None
    api_base: Optional[str] = None
    test_response: Optional[str] = None
    error: Optional[str] = None
