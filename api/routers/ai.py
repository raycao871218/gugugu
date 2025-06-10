"""
AI-related endpoints for the Gugugu API
"""
import os
import json
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from typing import List, Optional
from api.models.schemas import (
    AIRequest, AIStreamRequest, AIResponse, AIHealthResponse,
    RAGRequest, RAGResponse, DocumentListResponse, DocumentInfo,
    DocumentProcessRequest, DocumentProcessResponse
)
from api.core.config import get_ai_client, get_ai_model
from api.core.vector_store import vector_store

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


@router.post("/rag/chat", response_model=RAGResponse)
async def chat_with_rag(request: RAGRequest):
    """
    Chat with AI using RAG (Retrieval-Augmented Generation)
    
    Args:
        request (RAGRequest): RAG chat request with query and optional file name/path
        
    Returns:
        RAGResponse: AI response with relevant document sources
        
    Raises:
        HTTPException: 500 if AI service call fails
    """
    try:
        # Search for relevant document chunks (support both file_name and file_path)
        search_results = vector_store.search(
            query=request.message,
            file_path=request.file_path,
            file_name=request.file_name,
            top_k=request.top_k
        )
        
        # Build context from search results
        context_parts = []
        sources = []
        
        for result in search_results:
            context_parts.append(f"文档片段：{result['content']}")
            sources.append({
                'file_path': result['file_path'],
                'file_name': os.path.basename(result['file_path']),
                'chunk_index': result['chunk_index'],
                'similarity': result['similarity'],
                'content_preview': result['content'][:200] + "..." if len(result['content']) > 200 else result['content']
            })
        
        # Prepare the prompt with context
        if context_parts:
            context = "\n\n".join(context_parts)
            prompt = f"""基于以下文档内容回答用户问题。如果文档中没有相关信息，请说明并基于你的知识回答。

文档内容：
{context}

用户问题：{request.message}

请提供准确、有用的回答："""
        else:
            prompt = f"没有找到相关文档内容。请基于你的知识回答用户问题：{request.message}"
        
        # Call AI model
        client = get_ai_client()
        model = get_ai_model()
        
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=request.max_tokens,
            temperature=request.temperature
        )
        
        return RAGResponse(
            response=response.choices[0].message.content,
            model=model,
            sources=sources,
            usage=response.usage.dict() if response.usage else None
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"RAG服务调用失败: {str(e)}")


@router.get("/documents", response_model=DocumentListResponse)
async def list_documents():
    """
    List all documents in the vector store
    
    Returns:
        DocumentListResponse: List of all processed documents
    """
    try:
        files = vector_store.list_files()
        documents = [DocumentInfo(**file_info) for file_info in files]
        
        return DocumentListResponse(
            documents=documents,
            total_count=len(documents)
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取文档列表失败: {str(e)}")


@router.post("/documents/process", response_model=DocumentProcessResponse)
async def process_document(request: DocumentProcessRequest):
    """
    Process a document and add it to the vector store
    
    Args:
        request (DocumentProcessRequest): Document processing request with file_path or file_name
        
    Returns:
        DocumentProcessResponse: Processing result
        
    Raises:
        HTTPException: 400 if file not found, 500 if processing fails
    """
    try:
        # Validate request
        if not request.file_path and not request.file_name:
            raise HTTPException(status_code=400, detail="必须提供 file_path 或 file_name 参数")
        
        # Process the document
        success = vector_store.add_document(
            file_path=request.file_path,
            file_name=request.file_name,
            force_reprocess=request.force_reprocess
        )
        
        if success:
            # Get the resolved file path for response
            resolved_path = vector_store._resolve_file_path(request.file_path, request.file_name)
            
            # Get chunk count
            files = vector_store.list_files()
            chunk_count = next(
                (f['chunk_count'] for f in files if f['file_path'] == resolved_path),
                0
            )
            
            return DocumentProcessResponse(
                success=True,
                message=f"文档处理成功，生成了 {chunk_count} 个文档片段",
                file_path=resolved_path,
                chunk_count=chunk_count
            )
        else:
            resolved_path = vector_store._resolve_file_path(request.file_path, request.file_name)
            return DocumentProcessResponse(
                success=False,
                message="文档未发生变化，跳过处理",
                file_path=resolved_path
            )
            
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"文档处理失败: {str(e)}")


@router.post("/documents/process-splendor", response_model=DocumentProcessResponse)
async def process_splendor_document():
    """
    Process the Splendor game rules document using file name
    
    Returns:
        DocumentProcessResponse: Processing result for splendor.md
    """
    try:
        # Process using file name (much cleaner!)
        success = vector_store.add_document(file_name="splendor.md", force_reprocess=True)
        
        if success:
            # Get the resolved path for metadata
            resolved_path = vector_store._resolve_file_path(file_name="splendor.md")
            
            # Get chunk count
            files = vector_store.list_files()
            chunk_count = next(
                (f['chunk_count'] for f in files if f['file_path'] == resolved_path),
                0
            )
            
            return DocumentProcessResponse(
                success=True,
                message=f"璀璨宝石规则文档处理成功，生成了 {chunk_count} 个文档片段",
                file_path=resolved_path,
                chunk_count=chunk_count
            )
        else:
            resolved_path = vector_store._resolve_file_path(file_name="splendor.md")
            return DocumentProcessResponse(
                success=False,
                message="璀璨宝石规则文档处理失败",
                file_path=resolved_path
            )
            
    except ValueError as e:
        raise HTTPException(status_code=404, detail=f"璀璨宝石规则文档不存在: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"璀璨宝石规则文档处理失败: {str(e)}")


@router.post("/documents/process-catan", response_model=DocumentProcessResponse)
async def process_catan_document():
    """
    Process the Catan game rules document using file name
    
    Returns:
        DocumentProcessResponse: Processing result for catan.md
    """
    try:
        # Process using file name (much cleaner!)
        success = vector_store.add_document(file_name="catan.md", force_reprocess=True)
        
        if success:
            # Get the resolved path for metadata
            resolved_path = vector_store._resolve_file_path(file_name="catan.md")
            
            # Get chunk count
            files = vector_store.list_files()
            chunk_count = next(
                (f['chunk_count'] for f in files if f['file_path'] == resolved_path),
                0
            )
            
            return DocumentProcessResponse(
                success=True,
                message=f"卡坦岛规则文档处理成功，生成了 {chunk_count} 个文档片段",
                file_path=resolved_path,
                chunk_count=chunk_count
            )
        else:
            resolved_path = vector_store._resolve_file_path(file_name="catan.md")
            return DocumentProcessResponse(
                success=False,
                message="卡坦岛规则文档处理失败",
                file_path=resolved_path
            )
            
    except ValueError as e:
        raise HTTPException(status_code=404, detail=f"卡坦岛规则文档不存在: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"卡坦岛规则文档处理失败: {str(e)}")


@router.post("/documents/process-batch", response_model=List[DocumentProcessResponse])
async def process_documents_batch(request: List[DocumentProcessRequest]):
    """
    Process multiple documents in batch
    
    Args:
        request (List[DocumentProcessRequest]): List of document processing requests
        
    Returns:
        List[DocumentProcessResponse]: List of processing results
    """
    results = []
    
    for doc_request in request:
        try:
            # Validate request
            if not doc_request.file_path and not doc_request.file_name:
                results.append(DocumentProcessResponse(
                    success=False,
                    message="必须提供 file_path 或 file_name 参数",
                    file_path="unknown"
                ))
                continue
            
            # Process the document
            success = vector_store.add_document(
                file_path=doc_request.file_path,
                file_name=doc_request.file_name,
                force_reprocess=doc_request.force_reprocess
            )
            
            # Get the resolved file path for response
            resolved_path = vector_store._resolve_file_path(doc_request.file_path, doc_request.file_name)
            
            if success:
                # Get chunk count
                files = vector_store.list_files()
                chunk_count = next(
                    (f['chunk_count'] for f in files if f['file_path'] == resolved_path),
                    0
                )
                
                results.append(DocumentProcessResponse(
                    success=True,
                    message=f"文档处理成功，生成了 {chunk_count} 个文档片段",
                    file_path=resolved_path,
                    chunk_count=chunk_count
                ))
            else:
                results.append(DocumentProcessResponse(
                    success=False,
                    message="文档未发生变化，跳过处理",
                    file_path=resolved_path
                ))
                
        except ValueError as e:
            # File not found or validation error
            file_identifier = doc_request.file_name or doc_request.file_path or "unknown"
            results.append(DocumentProcessResponse(
                success=False,
                message=str(e),
                file_path=file_identifier
            ))
        except Exception as e:
            # Other processing errors
            file_identifier = doc_request.file_name or doc_request.file_path or "unknown"
            results.append(DocumentProcessResponse(
                success=False,
                message=f"文档处理失败: {str(e)}",
                file_path=file_identifier
            ))
    
    return results


@router.delete("/documents/{file_path:path}")
async def delete_document(file_path: str):
    """
    Remove a document from the vector store
    
    Args:
        file_path (str): Path of the document to remove
        
    Returns:
        dict: Deletion result
    """
    try:
        success = vector_store.remove_document(file_path)
        
        if success:
            return {"success": True, "message": f"文档 {file_path} 已从向量存储中删除"}
        else:
            return {"success": False, "message": f"文档 {file_path} 不存在于向量存储中"}
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"删除文档失败: {str(e)}")


@router.post("/rag/search", response_model=List[dict])
async def search_documents(
    query: str, 
    file_path: Optional[str] = None,
    file_name: Optional[str] = None,
    top_k: int = 5,
    min_similarity: float = 0.5
):
    """
    Search for relevant document chunks without AI response
    
    Args:
        query (str): Search query
        file_path (Optional[str]): Optional file path to limit search scope (for backward compatibility)
        file_name (Optional[str]): Optional file name to limit search scope (preferred)
        top_k (int): Number of top results to return
        min_similarity (float): Minimum similarity threshold
        
    Returns:
        List[dict]: List of relevant document chunks
    """
    try:
        results = vector_store.search(
            query=query, 
            file_path=file_path,
            file_name=file_name,
            top_k=top_k
        )
        
        # Filter by minimum similarity
        filtered_results = [r for r in results if r.get('similarity', 0) >= min_similarity]
        
        return filtered_results
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"文档搜索失败: {str(e)}")


@router.get("/documents/stats")
async def get_document_stats():
    """
    Get vector store statistics
    
    Returns:
        dict: Vector store statistics including file counts, chunks, and storage size
    """
    try:
        stats = vector_store.get_document_stats()
        return stats
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取统计信息失败: {str(e)}")


@router.post("/rag/chat-advanced", response_model=RAGResponse)
async def chat_with_advanced_rag(request: RAGRequest):
    """
    Enhanced RAG chat with reranked results and better context handling
    
    Args:
        request (RAGRequest): RAG chat request with query and optional file name/path
        
    Returns:
        RAGResponse: AI response with relevant document sources
    """
    try:
        # Search for relevant document chunks (support both file_name and file_path)
        search_results = vector_store.search(
            query=request.message,
            file_path=request.file_path,
            file_name=request.file_name,
            top_k=request.top_k * 2  # Get more results for reranking
        )
        
        # Rerank results for better relevance
        reranked_results = vector_store.rerank_results(search_results, request.message)[:request.top_k]
        
        # Build context from reranked results
        context_parts = []
        sources = []
        
        for result in reranked_results:
            context_parts.append(f"文档片段（相关度: {result.get('combined_score', result['similarity']):.3f}）：{result['content']}")
            sources.append({
                'file_path': result['file_path'],
                'file_name': os.path.basename(result['file_path']),
                'chunk_index': result['chunk_index'],
                'similarity': result['similarity'],
                'combined_score': result.get('combined_score', result['similarity']),
                'keyword_score': result.get('keyword_score', 0),
                'content_preview': result['content'][:200] + "..." if len(result['content']) > 200 else result['content']
            })
        
        # Determine game type from file path or content
        game_type = "通用"
        system_prompt = "你是桌游专家助手，精通各种桌游规则和策略。"
        
        if sources:
            file_name = os.path.basename(sources[0]['file_path']).lower()
            if 'splendor' in file_name:
                game_type = "璀璨宝石（Splendor）"
                system_prompt = "你是璀璨宝石（Splendor）桌游的专业助手，精通游戏规则和策略。"
            elif 'catan' in file_name:
                game_type = "卡坦岛（Catan）"
                system_prompt = "你是卡坦岛（Catan）桌游的专业助手，精通游戏规则和策略。"
        
        # Prepare enhanced prompt with context
        if context_parts:
            context = "\n\n".join(context_parts)
            prompt = f"""作为{game_type}游戏专家，请基于以下文档内容准确回答用户问题。请提供详细、实用的回答，并在适当时引用具体规则。

相关文档内容：
{context}

用户问题：{request.message}

请提供详细、准确的回答："""
        else:
            prompt = f"作为{game_type}游戏专家，没有找到直接相关的文档内容。请基于你的游戏知识回答用户问题：{request.message}"
        
        # Call AI model
        client = get_ai_client()
        model = get_ai_model()
        
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            max_tokens=request.max_tokens,
            temperature=request.temperature
        )
        
        return RAGResponse(
            response=response.choices[0].message.content,
            model=model,
            sources=sources,
            usage=response.usage.dict() if response.usage else None
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"高级RAG服务调用失败: {str(e)}")
