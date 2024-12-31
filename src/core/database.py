from motor.motor_asyncio import AsyncIOMotorClient
from config.settings import Settings

settings = Settings()

def init_db():
    client = AsyncIOMotorClient(settings.MONGO_URI)
    db = client.get_default_database()
    return db 