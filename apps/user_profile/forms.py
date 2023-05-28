from email.policy import default
from flask_wtf import FlaskForm
from wtforms import StringField,FileField,IntegerField,SelectField,SelectMultipleField
from wtforms.validators import Length,Optional,NumberRange
from flask_wtf.file import FileAllowed
from .models import Song

GENDER_CHOICES = [('Male', 'Male'), ('Female', 'Female'),('Other', 'Other')]
SONGS_CHOICES = [(str(song.id),song.title) for song in Song.query.all()]

class ProfileForm(FlaskForm):
    first_name = StringField(validators=[Optional()])
    last_name = StringField(validators=[Length(1, 64),Optional()])
    profile_image = FileField(validators=[FileAllowed(['jpg','jpeg','png','gif']),Optional()])
    age = IntegerField(validators=[NumberRange(min = 5, max = 90),Optional()])
    gender = SelectField(choices=GENDER_CHOICES)
    favourite_songs = SelectMultipleField(choices=SONGS_CHOICES)