from core.settings import settings
from core.settings.database import init_db

print(f"ENGINE_DB {settings.ENGINE_DB}")
init_db()
