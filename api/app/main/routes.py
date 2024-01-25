from flask import Blueprint, render_template
import random
from app.models import Exercise, ExerciseSchema
from datetime import datetime as dt
from sqlalchemy.orm import load_only


main = Blueprint('main', __name__)

exercises_schema = ExerciseSchema(many=True)

@main.route('/')
@main.route('/home')
def home():
    # Set random seed for one day, setting smaller time scales to 0
    # random.seed(dt.now().replace(second=0, microsecond=0).timestamp())
    # # random.seed(dt.now().replace(hour=0, minute=0, second=0, microsecond=0).timestamp())

    # Get random sample of four exercises
    all_exercises = Exercise.query.options(load_only(Exercise.id)).all()
    exercises = random.sample(all_exercises, k=4)
    exercises_json = exercises_schema.dumps(exercises)
    # exercises_json = jsonify(exercises_schema.dump(exercises)).get_json()

    print(exercises_json, type(exercises_json))


    # exercises_list = Exercise.query.limit(4).all()
    # exercises_json = jsonify(exercises_schema.dump(exercises_list)).get_json()
    # exercise_names = [ex['name'] for ex in exercises_json]
    # return exercise_names

    return render_template('home.html', title='Undisputed Fitness', exercises_json=exercises_json)
    # return exercises_json