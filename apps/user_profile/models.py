from sqlalchemy import ForeignKey
from crud import db

songs = db.Table('songs',
    db.Column('profile_id', ForeignKey('profile.id')),
    db.Column('song_id', ForeignKey('song.id'))
)

class Profile(db.Model):    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('user.id'),nullable=False)
    first_name = db.Column(db.String(40))
    last_name = db.Column(db.String(40))
    profile_image = db.Column(db.String(50))
    age = db.Column(db.Integer)
    gender = db.Column(db.String(15))
    favourite_song = db.relationship("Song",secondary=songs,backref="favourite_song")

    def __str__(self) -> str:
        return "%s" %(self.id)

class Song(db.Model):    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))

    def __str__(self) -> str:
        return "%s" %(self.id)