"""
Main application entry point for the Gugugu API
Modular FastAPI application with organized route handlers
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Import routers
from api.routers import health, ai
from api.core.config import get_debug_mode

# Create FastAPI application instance
app = FastAPI(
    title="Gugugu API",
    description="一个使用FastAPI构建的API服务，集成AI对话功能",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该设置具体的域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router)
app.include_router(ai.router)


# Root route
@app.get("/")
async def root():
    """
    Root endpoint with welcome message
    
    Returns:
        dict: Welcome message
    """
    return {"message": "欢迎使用Gugugu API!"}


# Application entry point
if __name__ == "__main__":
    reload = get_debug_mode()
    uvicorn.run(
        "main:app", 
        host="0.0.0.0", 
        port=8000, 
        reload=reload
    )