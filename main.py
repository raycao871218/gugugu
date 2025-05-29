from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn

# 创建FastAPI应用实例
app = FastAPI(
    title="Gugugu API",
    description="一个使用FastAPI构建的API服务",
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

# 数据模型
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

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
