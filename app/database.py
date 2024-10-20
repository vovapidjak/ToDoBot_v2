import logging
from app.config import settings
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

SQLALCHEMY_DATABASE_URL = settings.database_url

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


def init_db():
    inspector = inspect(engine)
    if not inspector.has_table("tasks.db"):  # Проверяем, существует ли таблица
        Base.metadata.create_all(bind=engine)  # Создает таблицы, если они не существуют
        print("База данных и таблица 'tasks' успешно созданы!")
    else:
        print("База данных и таблица 'tasks' уже существуют.")
