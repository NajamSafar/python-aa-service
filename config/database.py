import sqlalchemy
from databases import Database
from config.config import get_env

DATABASE_SERVER = 'database-server'

DATABASE_URL = get_env(DATABASE_SERVER, 'database-url', DATABASE_SERVER + 'database-url not configured')
database = Database(DATABASE_URL)
sqlalchemy_engine = sqlalchemy.create_engine(DATABASE_URL)

def get_database() -> Database:
    return database