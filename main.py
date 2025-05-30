from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
import os
from openai import OpenAI

# 创建FastAPI应用实例
app = FastAPI(
    title="Gugugu API",
    description="一个使用FastAPI构建的API服务，集成AI对话功能",
    version="1.0.0"
)

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该设置具体的域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 初始化 OpenAI 客户端
def get_ai_client():
    api_key = os.getenv("OPENAI_API_KEY")
    base_url = os.getenv("OPENAI_API_BASE")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is not set")
    return OpenAI(api_key=api_key, base_url=base_url)

# 数据模型
class AIRequest(BaseModel):
    message: str
    max_tokens: Optional[int] = 1000
    temperature: Optional[float] = 0.7

class AIResponse(BaseModel):
    response: str
    model: str
    usage: Optional[dict] = None
class Item(BaseModel):
    id: Optional[int] = None
    name: str
    description: Optional[str] = None
    price: float
    is_available: bool = True

class ItemCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    is_available: bool = True

# 模拟数据库
items_db = []
next_id = 1

# 根路由
@app.get("/")
async def root():
    return {"message": "欢迎使用Gugugu API!"}

# 健康检查
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# 获取所有物品
@app.get("/items", response_model=List[Item])
async def get_items():
    return items_db

# 根据ID获取物品
@app.get("/items/{item_id}", response_model=Item)
async def get_item(item_id: int):
    for item in items_db:
        if item.id == item_id:
            return item
    raise HTTPException(status_code=404, detail="物品未找到")

# 创建新物品
@app.post("/items", response_model=Item)
async def create_item(item: ItemCreate):
    global next_id
    new_item = Item(id=next_id, **item.dict())
    items_db.append(new_item)
    next_id += 1
    return new_item

# 更新物品
@app.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: int, item_update: ItemCreate):
    for i, item in enumerate(items_db):
        if item.id == item_id:
            updated_item = Item(id=item_id, **item_update.dict())
            items_db[i] = updated_item
            return updated_item
    raise HTTPException(status_code=404, detail="物品未找到")

# 删除物品
@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    for i, item in enumerate(items_db):
        if item.id == item_id:
            del items_db[i]
            return {"message": "物品已删除"}
    raise HTTPException(status_code=404, detail="物品未找到")

# AI 对话接口
@app.post("/ai/chat", response_model=AIResponse)
async def chat_with_ai(request: AIRequest):
    """
    与AI模型进行对话
    """
    try:
        client = get_ai_client()
        model = os.getenv("AI_MODEL", "deepseek-ai/DeepSeek-V3")
        
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

# AI 健康检查
@app.get("/ai/health")
async def ai_health_check():
    """
    检查AI服务连接状态
    """
    try:
        client = get_ai_client()
        model = os.getenv("AI_MODEL", "deepseek-ai/DeepSeek-V3")
        
        # 发送一个简单的测试请求
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": "Hello"}],
            max_tokens=10
        )
        
        return {
            "status": "healthy",
            "model": model,
            "api_base": os.getenv("OPENAI_API_BASE"),
            "test_response": response.choices[0].message.content
        }
        
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "model": os.getenv("AI_MODEL", "deepseek-ai/DeepSeek-V3"),
            "api_base": os.getenv("OPENAI_API_BASE")
        }

if __name__ == "__main__":
    import os
    reload = os.getenv("DEBUG", "False").lower() == "true"
    uvicorn.run(
        "main:app", 
        host="0.0.0.0", 
        port=8000, 
        reload=reload
    )
