import os
from dotenv import load_dotenv
from app.database import init_db
from app.entities.bot.bot import TelegramBot


def main():
    load_dotenv()
    TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    bot = TelegramBot(TOKEN)
    bot.run()


if __name__ == '__main__':
    init_db()
    main()
