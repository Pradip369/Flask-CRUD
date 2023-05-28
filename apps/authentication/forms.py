from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField
from wtforms.validators import InputRequired,Length,Regexp,EqualTo,Email,Optional
from .validators import validate_email,validate_uname

class RegisterForm(FlaskForm):
    username = StringField(
        validators=[
            InputRequired(),
            Length(3, 20, message="Please provide a valid user name"),
            validate_uname,
            Regexp(
                "^[A-Za-z][A-Za-z0-9_.]*$",
                0,
                "Usernames must have only letters, " "numbers, dots or underscores",
            ),
        ]
    )
    email = StringField(validators=[InputRequired(), Email(), Length(1, 64),validate_email])
    password = PasswordField(validators=[InputRequired(), Length(8, 72)])
    cpwd = PasswordField(
        validators=[
            InputRequired(),
            Length(8, 72),
            EqualTo("password", message="Passwords must match !"),
        ]
    )

class LoginForm(FlaskForm):
    email = StringField(validators=[InputRequired(), Email(), Length(1, 64)])
    password = PasswordField(validators=[InputRequired(), Length(min=8, max=72)])
    username = StringField(
        validators=[Optional()]
    )

class PasswordChangeForm(FlaskForm):
    current_password = PasswordField(validators=[InputRequired(), Length(8, 72)])
    new_password = PasswordField(validators=[InputRequired(), Length(8, 72)])
    confirm_new_password = PasswordField(
        validators=[
            InputRequired(),
            Length(8, 72),
            EqualTo("new_password", message="Passwords must match !"),
        ]
    )

class PasswordResetForm(FlaskForm):
    new_password = PasswordField(validators=[InputRequired(), Length(8, 72)])
    confirm_new_password = PasswordField(
        validators=[
            InputRequired(),
            Length(8, 72),
            EqualTo("new_password", message="Passwords must match !"),
        ]
    )