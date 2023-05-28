import os
from flask import Blueprint, flash, render_template,request,send_from_directory
from flask_login import login_required,current_user
from .models import Profile,Song
from crud import db,app,ALLOWED_EXTENSIONS
from .forms import ProfileForm
from werkzeug.utils import secure_filename

profile_views = Blueprint('profile_views', __name__)

def save_image(file):
    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return filename

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/media/<path:filename>')
def media(filename):
    return send_from_directory(
        app.config['UPLOAD_FOLDER'],
        filename,
        as_attachment=True
    )

@profile_views.route("/user_profile", methods=("GET", "POST"))
@login_required
def user_profile():
    form = ProfileForm()
    current_profile = Profile.query.filter_by(user_id=current_user.id).first()
    if form.validate_on_submit():
        try:
            file = form.profile_image.data
            orgnl_file = request.files['profile_image']
            if file and allowed_file(orgnl_file.filename):
                filename = save_image(orgnl_file)
                current_profile.profile_image = filename
            current_profile.first_name = form.first_name.data
            current_profile.last_name = form.last_name.data
            current_profile.age = form.age.data
            current_profile.gender = form.gender.data
            current_profile.favourite_song.append(int(form.favourite_songs.data[0]))
            db.session.add(current_profile)
            db.session.commit()
            flash("Profile updated successfully!!", "success")
        except Exception as e:
            print(e)
            pass

    return render_template("profile/my_profile.html",form=form,pf_data=current_profile)