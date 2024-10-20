import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score
# import joblib
#
# pipeline_category = joblib.load('app/entities/ML/category_model.pkl')
# pipeline_priority = joblib.load('app/entities/ML/priority_model.pkl')

# Загружаем данные
data = pd.read_csv('tasks.csv', sep=';')
data = pd.DataFrame(data)
data = data.drop(columns=['Unnamed: 4','Unnamed: 3' ])
print(data)
# Разделяем данные на задачи и метки категорий и приоритетов
X = data['Задача']  # Текст задач
y_category = data['Категория']  # Метки категорий
y_priority = data['Приоритет']  # Метки приоритетов

# Разделяем данные на тренировочные и тестовые наборы
X_train, X_test, y_train_category, y_test_category = train_test_split(X, y_category, test_size=0.2, random_state=42)
X_train_p, X_test_p, y_train_priority, y_test_priority = train_test_split(X, y_priority, test_size=0.2, random_state=42)
# Создаем конвейер для классификации категорий
pipeline_category = Pipeline([
    ('tfidf', TfidfVectorizer()),  # Преобразование текста в вектор
    ('clf', MultinomialNB())  # Классификатор
])

# Обучаем модель для классификации категорий
pipeline_category.fit(X_train, y_train_category)

# Прогнозируем категории на тестовом наборе
y_pred_category = pipeline_category.predict(X_test)

# Оцениваем точность
print(f'Точность классификации категорий: {accuracy_score(y_test_category, y_pred_category)}')
# Создаем конвейер для классификации приоритетов
pipeline_priority = Pipeline([
    ('tfidf', TfidfVectorizer()),  # Преобразование текста в вектор
    ('clf', MultinomialNB())  # Классификатор
])

# Обучаем модель для классификации приоритетов
pipeline_priority.fit(X_train_p, y_train_priority)

# Прогнозируем приоритеты на тестовом наборе
y_pred_priority = pipeline_priority.predict(X_test_p)

# Оцениваем точность
print(f'Точность классификации приоритетов: {accuracy_score(y_test_priority, y_pred_priority)}')
# Новая задача
new_task = ["срочно подготовиться к экзамену к понедельнику"]


# Сохранение обученных моделей в файлы
# joblib.dump(pipeline_category, 'category_model.pkl')
# joblib.dump(pipeline_priority, 'priority_model.pkl')

# Прогнозирование категории
print(f'Задача: {new_task}')
prob_category = pipeline_category.predict_proba(new_task)
predicted_category = pipeline_category.predict(new_task)
print(f'Категория задачи: {predicted_category[0]}, вероятность {np.max(prob_category)}')

# Прогнозирование приоритета
prob_priority = pipeline_priority.predict_proba(new_task)
predicted_priority = pipeline_priority.predict(new_task)
print(f'Приоритет задачи: {predicted_priority[0]}, вероятность {np.max(prob_priority)}')
