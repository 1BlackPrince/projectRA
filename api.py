from flask import Flask, request, jsonify
import joblib
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
import pandas as pd

app = Flask(__name__)

# Завантаження моделі ризику
model_risk = joblib.load('risk_model.pkl')

# Підключення до бази даних PostgreSQL
engine = create_engine('postgresql://postgres:2432@localhost/Project RA')

@app.route('/add_project', methods=['POST'])
def add_project():
    data = request.json
    project_id = data['projectid']
    work_volume = data['workvolume']
    tech_complexity = data['technicalcomplexity']
    team_size = data['teamsize']
    budget = data['budget']
    dependencies = data['dependencies']
    fact_complexity = data['factcomplexity']
    
    try:
        # Збереження даних проекту
        engine.execute(
            "INSERT INTO projects_data (projectid, workvolume, technicalcomplexity, teamsize, budget, dependencies, factcomplexity, data_source) VALUES (%s, %s, %s, %s, %s, %s, %s, 'operating')",
            (project_id, work_volume, tech_complexity, team_size, budget, dependencies, fact_complexity)
        )
        return jsonify({'message': 'Data inserted successfully'}), 200
    except SQLAlchemyError as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
