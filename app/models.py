from app import db

class ExerciseCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(25), unique=True, nullable=False)
    exercises = db.relationship('Exercise', backref='category', lazy=True)

    def __repr__(self):
        return f"ExerciseCategory('{self.id}', '{self.name}')"

class Exercise(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    desc = db.Column(db.String(500))
    work = db.Column(db.Integer, nullable=False)
    rest_seconds = db.Column(db.Integer, nullable=False)
    sets = db.Column(db.Integer, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    category_id = db.Column(db.Integer, db.ForeignKey(ExerciseCategory.id), nullable=False)

    def __repr__(self):
        return f"Exercise('{self.id}', '{self.name}', '{self.category}', 'Work: {self.work}', \
            'Rest: {self.rest_seconds}', 'Sets: {self.sets}')"