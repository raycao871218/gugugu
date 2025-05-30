"""
Items CRUD endpoints for the Gugugu API
"""
from fastapi import APIRouter, HTTPException
from typing import List
from api.models.schemas import Item, ItemCreate
from api.core.database import items_db

router = APIRouter(
    prefix="/items",
    tags=["items"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=List[Item])
async def get_items():
    """
    Get all items
    
    Returns:
        List[Item]: List of all items in the database
    """
    return items_db.get_all_items()


@router.get("/{item_id}", response_model=Item)
async def get_item(item_id: int):
    """
    Get a specific item by ID
    
    Args:
        item_id (int): The ID of the item to retrieve
        
    Returns:
        Item: The requested item
        
    Raises:
        HTTPException: 404 if item not found
    """
    item = items_db.get_item_by_id(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="物品未找到")
    return item


@router.post("/", response_model=Item)
async def create_item(item: ItemCreate):
    """
    Create a new item
    
    Args:
        item (ItemCreate): Item data to create
        
    Returns:
        Item: The created item with assigned ID
    """
    return items_db.create_item(item)


@router.put("/{item_id}", response_model=Item)
async def update_item(item_id: int, item_update: ItemCreate):
    """
    Update an existing item
    
    Args:
        item_id (int): The ID of the item to update
        item_update (ItemCreate): Updated item data
        
    Returns:
        Item: The updated item
        
    Raises:
        HTTPException: 404 if item not found
    """
    updated_item = items_db.update_item(item_id, item_update)
    if updated_item is None:
        raise HTTPException(status_code=404, detail="物品未找到")
    return updated_item


@router.delete("/{item_id}")
async def delete_item(item_id: int):
    """
    Delete an item by ID
    
    Args:
        item_id (int): The ID of the item to delete
        
    Returns:
        dict: Success message
        
    Raises:
        HTTPException: 404 if item not found
    """
    if not items_db.delete_item(item_id):
        raise HTTPException(status_code=404, detail="物品未找到")
    return {"message": "物品已删除"}
