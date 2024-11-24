from core.settings import settings
from core.settings.database import init_db
from core.utils.logger import logger

logger.info(f"ENGINE_DB {settings.ENGINE_DB}")
init_db()
