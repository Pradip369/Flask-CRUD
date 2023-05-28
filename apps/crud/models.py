from crud import db

class ToDoInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), unique=True, nullable=False)
    description = db.Column(db.Text(), unique=True, nullable=False)

    def __repr__(self):
        return '%r' % self.user_name