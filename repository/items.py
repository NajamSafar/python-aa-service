from config.database import get_database
from config.log import logger
from models.items import items
from schemas.items import Item

async def insert(item):
    try:
        item = item.dict()
        Database = get_database()

        data = {
            'name': item.get("name"),
            'price': item.get("price"),
            'company': item.get("company")
        }
        insert_query = items.insert().values(data)
        await Database.execute(insert_query)
    except Exception as e:
        logger.exception(f"Item is not inserted: {e}")
        raise e

async def update(item: Item, item_id: int):
    try:
        item = item.dict()
        Database = get_database()

        data = {
            'name': item.get("name"),
            'price': item.get("price"),
            'company': item.get("company")
        }
        query = items.update().values(data).where(items.c.id == item_id)
        await Database.execute(query)
    except Exception as e:
        logger.exception(f"Item is not updated: {e}")
        raise e

async def get_items():
    try:
        database = get_database()
        select_query = items.select()
        return await database.fetch_all(select_query)
    except Exception as e:
        raise e

async def get_item_by_id(id: int):
    try:
        database = get_database()
        select_query = items.select().where(items.c.id == id)
        return await database.fetch_one(select_query)
    except Exception as e:
        raise e

