from flask_login import UserMixin
from crud import db
from datetime import datetime
from crud import bcrypt
from sqlalchemy.orm import relationship

class User(UserMixin, db.Model):    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean(),default=False)
    hash_string = db.Column(db.String(255))
    created_on = db.Column(db.String(30),nullable=False,default=datetime.now())
    last_login = db.Column(db.DateTime,nullable=False,default=datetime.now())

    profile = relationship("Profile", uselist=False, backref="user",cascade="all, delete")

    def __repr__(self):
        return '<User %r>' % self.username

    def __str__(self) -> str:
        return '%s' %(self.username)

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password,password)

    def login_timestamp_update(self):
        self.last_login = datetime.now()
        db.session.commit()