import enum
from sqlalchemy import Enum


class Priority(enum.Enum):
    ВЫСОКИЙ = "ВЫСОКИЙ"  # Высокий приоритет
    НИЗКИЙ = "НИЗКИЙ"  # Низкий приоритет
