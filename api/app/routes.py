from flask import render_template, redirect, flash, url_for, request, jsonify
from app.forms import ExerciseCategoryForm, ExerciseForm
from app.models import Exercise, ExerciseCategory, ExerciseSchema
from app import app, db
import random
from datetime import datetime as dt
from sqlalchemy.orm import load_only, session
from sqlalchemy import select
import json


exercises_schema = ExerciseSchema(many=True)

@app.route('/')
@app.route('/home')
def home():
    # Set random seed for one day, setting smaller time scales to 0
    # random.seed(dt.now().replace(second=0, microsecond=0).timestamp())
    # # random.seed(dt.now().replace(hour=0, minute=0, second=0, microsecond=0).timestamp())

    # Get random sample of four (4) exercises
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



@app.route('/exercise_categories', methods=['GET', 'POST'])
def exercise_category():
    form = ExerciseCategoryForm()
    categories = ExerciseCategory.query.all()
    if form.validate_on_submit():
        new_category = ExerciseCategory(name=request.form['name'])
        db.session.add(new_category)
        db.session.commit()
        flash('New exercise category added.', 'success')
        return redirect(url_for('exercise_category'))
    return render_template('exercise_category.html', 
                           title='Exercise Categories', form=form,
                           categories=categories)

@app.route('/delete_exercise_category/<int:id>', methods=['GET', 'POST'])
def delete_exercise_category(id):
    category = ExerciseCategory.query.filter_by(id=id).first()
    if category:
        db.session.delete(category)
        db.session.commit()
        flash(f'"{category.name}" category deleted.', 'success')
    return redirect(url_for('exercise_category'))

@app.route('/update_exercise_category/<int:id>/<name>', methods=['GET', 'POST'])
def update_exercise_category(id, name):
    category = ExerciseCategory.query.get_or_404(id)
    form = ExerciseCategoryForm(name=name)
    form.submit.label.text = 'Update'
    if form.validate_on_submit():
        old_cat_name = category.name
        category.name = form.name.data
        db.session.commit()
        flash(f'"{old_cat_name}" category updated to "{category.name}".', 'success')
        return redirect(url_for('exercise_category'))
    return render_template('update_exercise_category.html', 
                           title='Update Exercise Catergory', form=form)
    # return redirect(url_for('exercise_category'))

@app.route('/exercises', methods=['GET', 'POST'])
def exercise():
    form = ExerciseForm()
    if form.validate_on_submit():
        exercise = Exercise(
            name=form.name.data,
            desc=form.desc.data,
            category=form.category.data,
            work=form.work.data,
            rest_seconds=form.rest_seconds.data,
            sets=form.sets.data,
            image_file=form.image_file.data
        )
        # TODO: handle images
        db.session.add(exercise)
        db.session.commit()
        flash('New exercise added', 'success')
        return redirect(url_for('exercise'))
    exercises = Exercise.query.all()
    return render_template('exercise.html', title='Exercises', 
                           form=form, exercises=exercises)


@app.route('/delete_exercise/<int:id>', methods=['GET', 'POST'])
def delete_exercise(id):
    exercise = Exercise.query.filter_by(id=id).first()
    if exercise:
        db.session.delete(exercise)
        db.session.commit()
        flash(f'"{exercise.name}" deleted.', 'success')
    return redirect(url_for('exercise'))