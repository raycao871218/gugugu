"""
Database simulation for items
This simulates a database using in-memory storage
In a real application, this would be replaced with actual database operations
"""
from typing import List, Optional
from api.models.schemas import Item, ItemCreate


class ItemsDatabase:
    """Simulated database for items using in-memory storage"""
    
    def __init__(self):
        self.items: List[Item] = []
        self.next_id: int = 1
    
    def get_all_items(self) -> List[Item]:
        """Get all items from the database"""
        return self.items
    
    def get_item_by_id(self, item_id: int) -> Optional[Item]:
        """Get a specific item by ID"""
        for item in self.items:
            if item.id == item_id:
                return item
        return None
    
    def create_item(self, item_data: ItemCreate) -> Item:
        """Create a new item"""
        new_item = Item(id=self.next_id, **item_data.dict())
        self.items.append(new_item)
        self.next_id += 1
        return new_item
    
    def update_item(self, item_id: int, item_data: ItemCreate) -> Optional[Item]:
        """Update an existing item"""
        for i, item in enumerate(self.items):
            if item.id == item_id:
                updated_item = Item(id=item_id, **item_data.dict())
                self.items[i] = updated_item
                return updated_item
        return None
    
    def delete_item(self, item_id: int) -> bool:
        """Delete an item by ID"""
        for i, item in enumerate(self.items):
            if item.id == item_id:
                del self.items[i]
                return True
        return False


# Global database instance
items_db = ItemsDatabase()
