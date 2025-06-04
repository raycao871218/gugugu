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


class RAGRequest(BaseModel):
    """Request model for RAG chat endpoints"""
    message: str
    file_name: Optional[str] = None  # 指定文档文件名，None表示搜索所有文档
    file_path: Optional[str] = None  # 向后兼容：指定文档路径，建议使用file_name
    max_tokens: Optional[int] = 1000
    temperature: Optional[float] = 0.7
    top_k: Optional[int] = 5  # 检索的相关片段数量


class RAGResponse(BaseModel):
    """Response model for RAG chat endpoints"""
    response: str
    model: str
    sources: List[dict]  # 引用的文档片段信息
    usage: Optional[dict] = None


class DocumentInfo(BaseModel):
    """Document information model"""
    file_path: str
    file_name: str
    chunk_count: int
    processed_at: str
    exists: bool


class DocumentListResponse(BaseModel):
    """Response model for document list"""
    documents: List[DocumentInfo]
    total_count: int


class DocumentProcessRequest(BaseModel):
    """Request model for document processing"""
    file_path: Optional[str] = None  # 向后兼容：完整文件路径
    file_name: Optional[str] = None  # 推荐：仅文件名（在预设目录中查找）
    force_reprocess: Optional[bool] = False


class DocumentProcessResponse(BaseModel):
    """Response model for document processing"""
    success: bool
    message: str
    file_path: str
    chunk_count: Optional[int] = None


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
