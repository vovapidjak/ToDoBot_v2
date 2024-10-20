from sqlalchemy import Column, Integer, String, Enum, DateTime, Boolean
from app.database import Base
from app.entities.tasks.priority import Priority


class TaskTable(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    description = Column(String, nullable=False)
    category = Column(String)  # Категория задачи: работа, учеба, личные дела
    priority = Column(Enum(Priority))  # Приоритет задачи: высокий или низкий
    deadline = Column(DateTime, nullable=True)  # Дедлайн задачи
    # advice_enabled = Column(Boolean, default=True)
