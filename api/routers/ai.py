"""
AI-related endpoints for the Gugugu API
"""
import os
import json
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from api.models.schemas import AIRequest, AIStreamRequest, AIResponse, AIHealthResponse
from api.core.config import get_ai_client, get_ai_model

router = APIRouter(
    prefix="/ai",
    tags=["ai"],
    responses={404: {"description": "Not found"}},
)


@router.post("/chat", response_model=AIResponse)
async def chat_with_ai(request: AIRequest):
    """
    Chat with AI model
    
    Args:
        request (AIRequest): Chat request containing message and parameters
        
    Returns:
        AIResponse: AI response with model information and usage stats
        
    Raises:
        HTTPException: 500 if AI service call fails
    """
    try:
        client = get_ai_client()
        model = get_ai_model()
        
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": request.message}
            ],
            max_tokens=request.max_tokens,
            temperature=request.temperature
        )
        
        return AIResponse(
            response=response.choices[0].message.content,
            model=model,
            usage=response.usage.dict() if response.usage else None
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI服务调用失败: {str(e)}")


@router.get("/health", response_model=AIHealthResponse)
async def ai_health_check():
    """
    Check AI service connection status
    
    Returns:
        AIHealthResponse: Status of AI service with test response
    """
    try:
        client = get_ai_client()
        model = get_ai_model()
        
        # Send a simple test request
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": "Hello"}],
            max_tokens=10
        )
        
        return AIHealthResponse(
            status="healthy",
            model=model,
            api_base=os.getenv("OPENAI_API_BASE"),
            test_response=response.choices[0].message.content
        )
        
    except Exception as e:
        return AIHealthResponse(
            status="unhealthy",
            error=str(e),
            model=get_ai_model(),
            api_base=os.getenv("OPENAI_API_BASE")
        )


@router.post("/chat/stream")
async def chat_with_ai_stream(request: AIStreamRequest):
    """
    Chat with AI model using streaming response
    
    Args:
        request (AIStreamRequest): Streaming chat request containing message and parameters
        
    Returns:
        StreamingResponse: Server-sent events stream with AI response chunks
        
    Raises:
        HTTPException: 500 if AI service call fails
    """
    try:
        client = get_ai_client()
        model = get_ai_model()
        
        def generate_stream():
            try:
                stream = client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "user", "content": request.message}
                    ],
                    max_tokens=request.max_tokens,
                    temperature=request.temperature,
                    stream=True
                )
                
                # Send initial event with metadata
                yield f"data: {json.dumps({'type': 'start', 'model': model})}\n\n"
                
                # Stream the response chunks
                for chunk in stream:
                    if hasattr(chunk, 'choices') and len(chunk.choices) > 0:
                        delta = chunk.choices[0].delta
                        if hasattr(delta, 'content') and delta.content:
                            chunk_data = {
                                'type': 'content',
                                'content': delta.content
                            }
                            yield f"data: {json.dumps(chunk_data)}\n\n"
                
                # Send completion event
                yield f"data: {json.dumps({'type': 'done'})}\n\n"
                
            except Exception as e:
                error_data = {
                    'type': 'error',
                    'error': f"AI服务调用失败: {str(e)}"
                }
                yield f"data: {json.dumps(error_data)}\n\n"
        
        return StreamingResponse(
            generate_stream(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "*",
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI流式服务初始化失败: {str(e)}")
