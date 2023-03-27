from config.database import get_database
from models.settings import settings

async def get_settings():
    try:
        database = get_database()
        select_query = settings.select()
        setting_list = await database.fetch_all(select_query)
        return convert_to_name_value_pair(setting_list)
    except Exception as e:
        raise

async def get_settings_by_name(name: str):
    try:
        database = get_database()
        select_query = settings.select().where(settings.c.name == name)
        return await database.fetch_all(select_query)
    except Exception as e:
        raise

def convert_to_name_value_pair(setting_list):
    key_value = {}
    for setting in setting_list:
        key_value[setting["name"]] = setting["value"]

    return key_value

