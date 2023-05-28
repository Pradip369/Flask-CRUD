from .models import User
from wtforms.validators import ValidationError


def validate_email(self, email):
    if User.query.filter_by(email=email.data).first():
        raise ValidationError("Email already registered!")

def validate_uname(self, uname):
    if User.query.filter_by(username=uname.data).first():
        raise ValidationError("Username already taken!")