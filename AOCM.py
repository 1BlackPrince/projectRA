import pandas as pd
import pickle  # Збереження моделі
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sqlalchemy import create_engine


# Підключення до бази даних
engine = create_engine('postgresql://postgres:2432@localhost:5432/Project RA')

# Завантаження даних
data = pd.read_sql_table('projects_data', engine)

# Кодування категорійних колонок
encoder = LabelEncoder()
data['technicalcomplexity'] = encoder.fit_transform(data['technicalcomplexity'])

# Обрахунок рівня ризику (якщо потрібно)
data['risk_level'] = (data['technicalcomplexity'] * 0.5 + data['dependencies'] * 0.3 + data['budget'] / 100000 * 0.2).astype(int)

# Вхідні дані для моделі
X = data[['workvolume', 'technicalcomplexity', 'teamsize', 'budget', 'dependencies']]
y = data['factcomplexity']

# Розділення на тренувальні та тестові дані
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Створення та тренування моделі RandomForest
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Збереження моделі
with open('model_AOCM.pkl', 'wb') as file:
    pickle.dump(model, file)

# Збереження результатів в базу даних
data['predicted_complexity'] = model.predict(X)
data.to_sql('projects_complexity', engine, if_exists='replace', index=False)
