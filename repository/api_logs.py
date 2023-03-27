from config.database import get_database
from config.log import logger
from models.api_logs import api_logs

async def insert(log_object):
    try:
        log_object = log_object.dict()
        Database = get_database()

        log_info = {
            'channel': log_object.get("channel"),
            'request_url': log_object.get("request_url"),
            'request_method': log_object.get("request_method"),
            'params': log_object.get("params"),
            'request_body': log_object.get("request_body"),
            'response_body': log_object.get("response_body"),
            'status_code': log_object.get("status_code"),
            'api_call_duration': log_object.get("api_call_duration"),
            'request_time': log_object.get("request_time")
        }
        insert_query = api_logs.insert().values(log_info)
        await Database.execute(insert_query)
    except Exception as e:
        logger.exception(f"API log is not inserted: {e}")