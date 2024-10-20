import os
from dotenv import load_dotenv


class Settings():
    load_dotenv()
    database_url = os.getenv("DATABASE_URL")


settings = Settings()
