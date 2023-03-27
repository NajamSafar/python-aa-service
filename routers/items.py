from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse

from auth import get_api_key
from services import items
from config.log import logger
from schemas.items import Item

router = APIRouter(
    prefix="/items",
    tags=["items"],
    dependencies=[Depends(get_api_key)],
    responses={404: {"description": "Not found"}},
)

@router.get("/")
async def read_items():
    try:
        item_list = await items.get()
        return item_list
    except Exception as e:
        logger.exception(f"Exception occurred {e}")
        return JSONResponse(status_code=500, content={"status": "FAILED", "error": f"{e.args[0]}"})

@router.get("/{item_id}")
async def read_item(item_id: int):
    try: 
        item = await items.get(item_id)
        
        if item is None:
            logger.info("item is not found for ID: " + str(item_id))
            raise HTTPException(status_code=404, detail="Item not found")
        return item
    except Exception as e:
        logger.exception(f"Exception occurred {e}")
        return JSONResponse(status_code=500, content={"status": "FAILED", "error": f"{e.args[0]}"})

@router.put(
    "/{item_id}",
    tags=["custom"],
    responses={403: {"description": "Operation forbidden"}},
)
async def update_item(item_id: str, request_info: Item):
    try:
        item = await items.get(item_id)
        
        if item is None:
            logger.info("item is not found for ID: " + str(item_id))
            raise HTTPException(status_code=404, detail="Item not found")

        await items.update(request_info, item_id)
        return {"status": "SUCCESS", "message": "Item has been updated"}

    except Exception as e:
        logger.exception(f"Exception occurred {e}")
        return JSONResponse(status_code=500, content={"status": "FAILED", "error": f"{e.args[0]}"})