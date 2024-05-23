import sys

from loguru import logger

from core.settings import settings


class LoggerConfig:


    @staticmethod
    def load_format():
        _custom_format = (
        "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
        "<level>{level: <8}</level> | "
        "<yellow>{extra[trace_id]}</yellow> | "
        "<magenta>{extra[caller_id]}</magenta> | "
        "<green>{extra[project_id]}</green> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
        "<level>{message}</level> | "
    )
        logger.configure(extra={"trace_id": None, "caller_id": None, "project_id": settings.PROJECT_ID})
        logger.remove()
        logger.add(sys.stdout, colorize=True, format=_custom_format)
