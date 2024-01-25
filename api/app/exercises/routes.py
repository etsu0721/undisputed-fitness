from flask import Blueprint, render_template, redirect, flash, url_for, request
from app.exercises.forms import ExerciseCategoryForm, ExerciseForm
from app.models import Exercise, ExerciseCategory
from app import db

exercises = Blueprint('exercises', __name__)

@exercises.route('/exercise_categories', methods=['GET', 'POST'])
def exercise_category():
    form = ExerciseCategoryForm()
    categories = ExerciseCategory.query.all()
    if form.validate_on_submit():
        new_category = ExerciseCategory(name=request.form['name'])
        db.session.add(new_category)
        db.session.commit()
        flash('New exercise category added.', 'success')
        return redirect(url_for('exercises.exercise_category'))
    return render_template('exercise_category.html', 
                           title='Exercise Categories', form=form,
                           categories=categories)


@exercises.route('/delete_exercise_category/<int:id>', methods=['GET', 'POST'])
def delete_exercise_category(id):
    category = ExerciseCategory.query.filter_by(id=id).first()
    if category:
        db.session.delete(category)
        db.session.commit()
        flash(f'"{category.name}" category deleted.', 'success')
    return redirect(url_for('exercises.exercise_category'))


@exercises.route('/update_exercise_category/<int:id>/<name>', methods=['GET', 'POST'])
def update_exercise_category(id, name):
    category = ExerciseCategory.query.get_or_404(id)
    form = ExerciseCategoryForm(name=name)
    form.submit.label.text = 'Update'
    if form.validate_on_submit():
        old_cat_name = category.name
        category.name = form.name.data
        db.session.commit()
        flash(f'"{old_cat_name}" category updated to "{category.name}".', 'success')
        return redirect(url_for('exercises.exercise_category'))
    return render_template('update_exercise_category.html', 
                           title='Update Exercise Catergory', form=form)
    # return redirect(url_for('exercise_category'))


@exercises.route('/exercises', methods=['GET', 'POST'])
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
        return redirect(url_for('exercises.exercise'))
    exercises = Exercise.query.all()
    return render_template('exercise.html', title='Exercises', 
                           form=form, exercises=exercises)


@exercises.route('/delete_exercise/<int:id>', methods=['GET', 'POST'])
def delete_exercise(id):
    exercise = Exercise.query.filter_by(id=id).first()
    if exercise:
        db.session.delete(exercise)
        db.session.commit()
        flash(f'"{exercise.name}" deleted.', 'success')
    return redirect(url_for('exercises.exercise'))