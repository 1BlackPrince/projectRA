import pandas as pd
from sqlalchemy import create_engine
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.metrics import classification_report, accuracy_score
import joblib


# Підключення до бази даних
engine = create_engine('postgresql://postgres:2432@localhost/Project RA')

# Завантаження даних
data = pd.read_sql_table('projects_data', engine)
complexity_data = pd.read_sql_table('projects_complexity', engine)

# Об'єднання таблиць за projectid
data = data.merge(complexity_data[['projectid', 'risk_level']], on='projectid', how='left')

# Підготовка даних
data['technicalcomplexity'] = data['technicalcomplexity'].map({'Low': 0, 'Medium': 1, 'High': 2})
data['factcomplexity'] = data['factcomplexity'].map({'Low': 0, 'Medium': 1, 'High': 2})
X = data[['workvolume', 'technicalcomplexity', 'teamsize', 'budget', 'dependencies', 'factcomplexity']]
y = data['risk_level']

# Розділення даних на тренувальні та тестові
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

# Створення пайплайну для масштабування та логістичної регресії
pipe = make_pipeline(
    StandardScaler(),
    LogisticRegression(max_iter=1000, class_weight='balanced')
)

# Навчання моделі
pipe.fit(X_train, y_train)

# Оцінка моделі
predictions = pipe.predict(X_test)
probabilities = pipe.predict_proba(X_test)[:, 1]  # Взяття ймовірності для класу 1

# Збереження результатів
results = pd.DataFrame({
    'projectid': X_test.index,
    'predicted_risk': predictions,
    'risk_probability': probabilities  # Додано ймовірність ризику
})
results.to_sql('projects_risk', engine, if_exists='replace', index=False)

print(classification_report(y_test, predictions))
print("Accuracy:", accuracy_score(y_test, predictions))

# Збереження моделі
joblib.dump(pipe, 'risk_model.pkl')
