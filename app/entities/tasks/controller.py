import joblib
from app.entities.tasks.models import TaskTable
from app.entities.tasks.priority import Priority
from app.database import SessionLocal
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime


class Task:
    model = TaskTable
    db = SessionLocal()

    # @classmethod
    # def toggle_advice(cls, user_id):
    #     """Переключает состояние советов для пользователя."""
    #     user = cls.db.query(cls.model).filter_by(id=user_id).first()
    #     if user:
    #         user.advice_enabled = not user.advice_enabled
    #         cls.db.commit()
    #         return user.advice_enabled
    #     return None
    #
    # @classmethod
    # def is_advice_enabled(cls, user_id):
    #     """Проверяет, включены ли советы для пользователя."""
    #     user = cls.db.query(cls.model).filter_by(id=user_id).first()
    #     if user:
    #         return user.advice_enabled
    #     return True  # По умолчанию советы включены



    @classmethod
    def add_task(cls, user_id, description, deadline=None):
        """Добавляет задачу с предсказанными категорией, приоритетом и дедлайном по умолчанию."""
        pipeline_category = joblib.load('/Users/vovapidj/PycharmProjects/ToDoBot_v2/app/entities/ML/category_model.pkl')
        pipeline_priority = joblib.load('/Users/vovapidj/PycharmProjects/ToDoBot_v2/app/entities/ML/priority_model.pkl')

        predicted_category = pipeline_category.predict([description])[0]
        category_str = str(predicted_category)
        predicted_priority = pipeline_priority.predict([description])[0]
        priority_enum = Priority[predicted_priority.upper()]

        # Устанавливаем дедлайн по умолчанию на None
        new_task = cls.model(
            user_id=user_id,
            description=description,
            category=category_str,
            priority=priority_enum,
            deadline=None  # дедлайн по умолчанию
        )

        try:
            cls.db.add(new_task)
            cls.db.commit()
            return True, f"Задача '{description}' добавлена!\nКатегория: {category_str}\nПриоритет: {predicted_priority}."
        except SQLAlchemyError:
            cls.db.rollback()
            return False, "Произошла ошибка при добавлении задачи."
        finally:
            cls.db.close()

    @classmethod
    def get_tasks(cls, user_id):
        """Получает список задач пользователя."""
        try:
            tasks = cls.db.query(cls.model).filter_by(user_id=user_id).all()
            return tasks
        finally:
            cls.db.close()

    @classmethod
    def get_tasks_by_priority(cls, user_id, priority):
        """Получает задачи по приоритету."""
        try:
            priority_enum = Priority[priority.upper()]
            tasks = cls.db.query(cls.model).filter_by(user_id=user_id, priority=priority_enum).all()
            return tasks
        finally:
            cls.db.close()

    @classmethod
    def get_tasks_by_category(cls, user_id, category):
        """Получает задачи по категории, нечувствительные к регистру."""
        try:
            # Приводим категорию к нижнему регистру для сравнения
            tasks = cls.db.query(cls.model).filter_by(user_id=user_id).all()
            matching_tasks = [task for task in tasks if task.category.lower() == category.lower()]
            return matching_tasks
        finally:
            cls.db.close()

    @classmethod
    def delete_task(cls, user_id, task_index):
        """Удаляет задачу по индексу для указанного пользователя."""
        tasks = cls.db.query(cls.model).filter_by(user_id=user_id).all()

        if not tasks or task_index >= len(tasks):
            return False, "Некорректный номер задачи."

        task_to_delete = tasks[task_index]

        try:
            cls.db.delete(task_to_delete)
            cls.db.commit()
            return True, f"Задача '{task_to_delete.description}' удалена."
        except SQLAlchemyError as e:
            cls.db.rollback()
            return False, "Произошла ошибка при удалении задачи."
        finally:
            cls.db.close()

    @classmethod
    def update_task(cls, user_id, task_index, new_description=None, new_category=None, new_priority=None,
                    new_deadline=None):
        """Обновляет задачу."""
        tasks = cls.db.query(cls.model).filter_by(user_id=user_id).all()

        if not tasks or task_index >= len(tasks):
            return False, "Некорректный номер задачи."

        task_to_update = tasks[task_index]

        if new_description:
            task_to_update.description = new_description
        if new_category:
            task_to_update.category = new_category
        if new_priority:
            task_to_update.priority = Priority[new_priority.upper()]
        if new_deadline:
            try:
                task_to_update.deadline = datetime.strptime(new_deadline, "%d.%m.%Y %H:%M")
            except ValueError:
                return False, "Неверный формат дедлайна. Используйте 'дд.мм.гггг чч:мм'."

        try:
            cls.db.commit()
            return True, f"Задача '{task_to_update.description}' обновлена."
        except SQLAlchemyError:
            cls.db.rollback()
            return False, "Произошла ошибка при обновлении задачи."
        finally:
            cls.db.close()

    @classmethod
    def clear_tasks(cls, user_id):
        """Очищает все задачи для пользователя."""
        tasks = cls.db.query(cls.model).filter_by(user_id=user_id).delete()
        cls.db.commit()
        cls.db.close()
