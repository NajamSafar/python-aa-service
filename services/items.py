from repository import items
from schemas.items import Item

async def get():
    return await items.get_items()

async def get(item_id: int):
    return await items.get_item_by_id(item_id)

async def update(item: Item, item_id: int):
    return await items.update(item, item_id)