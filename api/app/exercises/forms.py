from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, Length, NumberRange, ValidationError
from wtforms_sqlalchemy.fields import QuerySelectField
from app.models import ExerciseCategory


def exercise_categories():
    return ExerciseCategory.query.all()

class ExerciseCategoryForm(FlaskForm):
    name = StringField('Exercise Category',
                       validators=[DataRequired(), Length(max=25)])
    submit = SubmitField('Create')

    def validate_name(self, name):
        category = ExerciseCategory.query.filter_by(name=name.data).first()
        if category:
            raise ValidationError('Category already exists.')


class ExerciseForm(FlaskForm):
    name = StringField('Exercise', validators=[DataRequired(), Length(max=120)])
    desc = TextAreaField('Description', 
                         validators=[DataRequired(), Length(max=500)])
    category = QuerySelectField('Category', query_factory=exercise_categories, 
                                get_label='name', validators=[DataRequired()])
    work = IntegerField('Work (based on category units)', 
                        validators=[DataRequired(), NumberRange(min=1)])
    rest_seconds = IntegerField('Rest (seconds)', 
                                validators=[DataRequired(), NumberRange(min=0)])
    sets = IntegerField('Sets', validators=[DataRequired(), NumberRange(min=1)])
    image_file = FileField('Exercise Image / GIF', 
                           validators=[FileAllowed(['jpg', 'png', 'gif'])])
    submit = SubmitField('Create')
