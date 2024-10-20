from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters, CallbackQueryHandler
from datetime import datetime, timedelta
from app.entities.tasks.controller import Task
from app.entities.tasks.priority import Priority
import random
import os
from dotenv import load_dotenv
from apscheduler.schedulers.background import BackgroundScheduler
import pytz
import sys


class TelegramBot:
    def __init__(self, token):
        self.updater = Updater(token, use_context=True)
        self.dispatcher = self.updater.dispatcher
        self.last_tip = None
        # self.scheduler = BackgroundScheduler()
        # self.scheduler.add_job(self.check_deadlines, 'interval', minutes=1)
        # self.timezone = pytz.timezone('Europe/Moscow')
        # self.scheduler.start()
        self._register_handlers()

    # def check_deadlines(self, update):
    #     """Проверяет дедлайны и отправляет уведомления, если дедлайн скоро наступит."""
    #     user_id = update.message.from_user.id
    #     tasks = Task.get_tasks(user_id)  # Получаем все задачи
    #     # timezone = pytz.timezone()  # Укажите свою временную зону
    #     now = datetime.now(self.timezone)
    #
    #     for task in tasks:
    #         if task.deadline:
    #             time_remaining = task.deadline - now
    #             if timedelta(hours=1) > time_remaining >= timedelta(minutes=0):  # Дедлайн наступит через час
    #                 update.message.reply_text(
    #                     chat_id=task.user_id,
    #                     text=f"⚠️ Ваша задача '{task.description}' истекает через {time_remaining}. "
    #                          f"Сделайте ее как можно скорее!"
    #                 )

    # def stop(self):
    #     """Останавливает планировщик при завершении работы бота."""
    #     self.scheduler.shutdown()

    def _register_handlers(self):
        # Регистрация команд
        self.dispatcher.add_handler(CommandHandler("start", self.start))
        self.dispatcher.add_handler(CommandHandler("add", self.add_task))
        self.dispatcher.add_handler(CommandHandler("list", self.list_tasks))
        self.dispatcher.add_handler(CommandHandler("delete", self.delete_task))
        self.dispatcher.add_handler(CommandHandler("clear", self.clear_tasks))
        self.dispatcher.add_handler(CommandHandler("priority", self.tasks_by_priority))
        self.dispatcher.add_handler(CommandHandler("category", self.tasks_by_category))
        self.dispatcher.add_handler(CommandHandler("update_description", self.update_task_description))
        self.dispatcher.add_handler(CommandHandler("update_category", self.update_task_category))
        self.dispatcher.add_handler(CommandHandler("update_priority", self.update_task_priority))
        self.dispatcher.add_handler(CommandHandler("update_deadline", self.update_task_deadline))
        # self.dispatcher.add_handler(CommandHandler("toggle_advice", self.toggle_advice))
        # self.dispatcher.add_handler(CommandHandler("restart", self.restart))
        self.dispatcher.add_handler(CommandHandler("help", self.help))  # Добавляем обработчик команды /help

    def start(self, update, context):
        update.message.reply_text(
            "Привет! Я ваш PlanManBot. Используйте команды:\n"
            "/add - добавить задачу\n"
            "/list - показать все задачи\n"
            "/delete - удалить задачу\n"
            "/clear - очистить все задачи\n"
            "/priority [высокий|низкий] - показать задачи по приоритету\n"
            "/category [работа|учеба|личные дела] - показать задачи по категории\n"
            "/update_description [index] [новое описание] - изменить описание задачи\n"
            "/update_category [index] [работа|учеба|личные дела] - изменить категорию задачи\n"
            "/update_priority [index] [высокий|низкий] - изменить приоритет задачи\n"
            "/update_deadline [index] [дд.мм.гггг чч:мм] - изменить дедлайн задачи\n"
            # "/restart - перезапустить бота\n"
            "/help - показать список доступных команд"
            # "/toggle_advice - включить или отключить советы по управлению временем"
        )

        # TODO: написать /restart для бота

    def help(self, update, context):
        update.message.reply_text(
            "Список доступных команд:\n"
            "/start - начать работу с ботом\n"
            "/add - добавить задачу\n"
            "/list - показать все задачи\n"
            "/delete - удалить задачу\n"
            "/clear - очистить все задачи\n"
            "/priority [высокий|низкий] - показать задачи по приоритету\n"
            "/category [работа|учеба|личные дела] - показать задачи по категории\n"
            "/update_description [index] [новое описание] - изменить описание задачи\n"
            "/update_category [index] [работа|учеба|личные дела] - изменить категорию задачи\n"
            "/update_priority [index] [высокий|низкий] - изменить приоритет задачи\n"
            "/update_deadline [index] [дд.мм.гггг чч:мм] - изменить дедлайн задачи\n"
            # "/restart - перезапустить бота\n"
            "/help - показать список доступных команд"
        )

    def send_time_management_tip(self, chat_id, task_count, context):
        # if not Task.is_advice_enabled(chat_id):
        #     return
        tips = [
            "Попробуйте метод Pomodoro. Это техника управления временем, при которой вы работаете 25 минут, а затем делаете перерыв на 5 минут. После четырех таких циклов сделайте более длительный перерыв на 15-30 минут. Этот метод помогает улучшить концентрацию и избежать выгорания.",
            "Используйте метод ABCDE для расстановки приоритетов. Присвойте каждой задаче одну из категорий: A – очень важные задачи, B – важные задачи, C – менее важные задачи, D – задачи, которые можно делегировать, и E – задачи, которые можно исключить. Это поможет вам лучше управлять своими ресурсами.",
            "Попробуйте делегировать менее важные задачи. Если вы чувствуете перегрузку, делегирование помогает сосредоточиться на наиболее приоритетных задачах. Подумайте, кто из ваших коллег или знакомых может выполнить менее критичные задачи.",
            "Разбейте большие задачи на более мелкие. Часто сложные задачи кажутся непреодолимыми, но если их разбить на небольшие подзадачи, они становятся более управляемыми и легко выполнимыми.",
            "Сосредоточьтесь на одной задаче за раз. Многозадачность снижает продуктивность, потому что ваше внимание рассеивается. Лучше завершить одну задачу полностью, прежде чем переходить к следующей.",
            "Запланируйте самые важные дела на первую половину дня. У большинства людей уровень энергии выше в начале дня, поэтому это идеальное время для решения сложных задач. Начните с наиболее приоритетных дел, чтобы получить максимальную отдачу."
        ]

        available_tips = [tip for tip in tips if tip != self.last_tip]

        # Выбираем случайный совет из оставшихся
        tip = random.choice(available_tips)

        # Сохраняем выбранный совет как последний
        self.last_tip = tip

        # Сообщение о количестве задач с высоким приоритетом
        context.bot.send_message(chat_id,
                                 f"У вас накопилось {task_count} задач с высоким приоритетом. Возможно, стоит пересмотреть планирование.\n\nСовет по управлению временем:\n{tip}")

    # def toggle_advice(self, update, context):
    #     """Включает или отключает советы по управлению временем для пользователя."""
    #     chat_id = update.message.chat_id
    #     advice_enabled = Task.toggle_advice(chat_id)
    #
    #     if advice_enabled:
    #         update.message.reply_text("Советы по управлению временем включены.")
    #     else:
    #         update.message.reply_text("Советы по управлению временем отключены.")

    def add_task(self, update, context):
        user_id = update.message.from_user.id
        description = " ".join(context.args)
        if not description:
            update.message.reply_text("Введите описание задачи после команды /add.")
            return

        success, response = Task.add_task(user_id, description)
        # Ответ пользователю с информацией о добавлении задачи
        if success:
            update.message.reply_text(f"{response}")
            # tips_enabled = Task.is_advice_enabled(user_id)
            # if tips_enabled:
            high_priority_tasks = Task.get_tasks_by_priority(user_id, 'высокий')
            if len(high_priority_tasks) >= 5:
                self.send_time_management_tip(update.message.chat.id, len(high_priority_tasks), context)
        else:
            update.message.reply_text(f"Ошибка: {response}")

    def list_tasks(self, update, context):
        user_id = update.message.from_user.id
        tasks = Task.get_tasks(user_id)

        if tasks:
            message = "Ваши задачи:\n" + "\n".join(
                f"{i + 1}. {task.description}\n     Категория: {task.category}\n     Приоритет: {task.priority.name}\n     Дедлайн: {task.deadline.strftime('%d.%m.%Y %H:%M') if task.deadline else 'без дедлайна'}\n----------------------------------"
                for i, task in enumerate(tasks)
            )
            update.message.reply_text(message)
        else:
            update.message.reply_text("У вас нет задач.")

    def delete_task(self, update, context):
        user_id = update.message.from_user.id
        try:
            task_index = int(context.args[0]) - 1
        except (IndexError, ValueError):
            update.message.reply_text("Пожалуйста, укажите корректный номер задачи для удаления.")
            return

        success, response = Task.delete_task(user_id, task_index)
        if success:
            update.message.reply_text(response)
        else:
            update.message.reply_text(response)

    def tasks_by_priority(self, update, context):
        user_id = update.message.from_user.id
        try:
            priority = context.args[0].lower()
        except IndexError:
            update.message.reply_text("Пожалуйста, укажите приоритет: 'высокий' или 'низкий'.")
            return

        tasks = Task.get_tasks_by_priority(user_id, priority)
        if tasks:
            message = f"Ваши задачи с приоритетом '{priority}':\n" + "\n".join(
                f"{i + 1}. {task.description} - {task.category}" for i, task in enumerate(tasks))
            update.message.reply_text(message)
        else:
            update.message.reply_text(f"Нет задач с приоритетом '{priority}'.")

    def tasks_by_category(self, update, context):
        user_id = update.message.from_user.id
        try:
            # Приводим категорию к нижнему регистру
            category = " ".join(context.args).lower()
        except IndexError:
            update.message.reply_text("Пожалуйста, укажите категорию: 'работа', 'учеба' или 'личные дела'.")
            return

        tasks = Task.get_tasks_by_category(user_id, category)
        if tasks:
            message = f"Ваши задачи в категории '{category}':\n" + "\n".join(
                f"{i + 1}. {task.description} - Приоритет: {task.priority.name}" for i, task in enumerate(tasks))
            update.message.reply_text(message)
        else:
            update.message.reply_text(f"Нет задач в категории '{category}'.")

    def update_task_description(self, update, context):
        user_id = update.message.from_user.id
        try:
            task_index = int(context.args[0]) - 1  # Индекс задачи
            new_description = " ".join(context.args[1:])  # Описание задачи может состоять из нескольких слов
        except (IndexError, ValueError):
            update.message.reply_text("Пожалуйста, укажите корректный индекс задачи и новое описание.")
            return

        success, response = Task.update_task(user_id, task_index, new_description=new_description)
        update.message.reply_text(response)

    def update_task_category(self, update, context):
        user_id = update.message.from_user.id
        try:
            task_index = int(context.args[0]) - 1  # Индекс задачи
            new_category = " ".join(context.args[1:])  # Категория может быть из нескольких слов
        except (IndexError, ValueError):
            update.message.reply_text("Пожалуйста, укажите корректный индекс задачи и категорию.")
            return

        success, response = Task.update_task(user_id, task_index, new_category=new_category)
        update.message.reply_text(response)

    def update_task_priority(self, update, context):
        user_id = update.message.from_user.id
        try:
            task_index = int(context.args[0]) - 1  # Индекс задачи
            new_priority = context.args[1].lower()  # Приоритет может быть либо "высокий", либо "низкий"
        except (IndexError, ValueError):
            update.message.reply_text(
                "Пожалуйста, укажите корректный индекс задачи и приоритет ('высокий' или 'низкий').")
            return

        success, response = Task.update_task(user_id, task_index, new_priority=new_priority)
        update.message.reply_text(response)

    def update_task_deadline(self, update, context):
        user_id = update.message.from_user.id
        try:
            task_index = int(context.args[0]) - 1
            new_deadline = " ".join(context.args[1:])
        except (IndexError, ValueError):
            update.message.reply_text("Пожалуйста, укажите номер задачи и новый дедлайн в формате 'дд.мм.гггг чч:мм'.")
            return

        success, response = Task.update_task(user_id, task_index, new_deadline=new_deadline)
        update.message.reply_text(response)

    def clear_tasks(self, update, context):
        user_id = update.message.from_user.id
        Task.clear_tasks(user_id)
        update.message.reply_text("Все задачи удалены.")

    def run(self):
        self.updater.start_polling()
        self.updater.idle()
