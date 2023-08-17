from flask import render_template, redirect, flash, url_for, request
from app.forms import ExerciseCategoryForm, ExerciseForm
from app.models import Exercise, ExerciseCategory
from app import app, db


@app.route('/')
@app.route('/home')
def home():
    exercises = Exercise.query.all()
    return render_template('home.html', title='Undisputed Fitness', 
                           exercises=exercises)


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
    # TODO: implement Create for exercises and handle images
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
        db.session.add(exercise)
        db.session.commit()
        flash('New exercise category added', 'success')
        return redirect(url_for('home'))
    return render_template('exercise.html', title='Exercises', 
                           form=form)

