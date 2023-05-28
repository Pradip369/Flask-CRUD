from flask import Blueprint, flash, redirect, render_template,url_for,request
from flask_login import login_user,login_required,logout_user,current_user
from .models import User
from crud import db,login_manager,mail
from .forms import LoginForm,RegisterForm,PasswordChangeForm,PasswordResetForm
import random
import string
from flask_mail import Message
from ..user_profile.models import Profile


auth_views = Blueprint('auth_views', __name__)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@auth_views.route("/register", methods=("GET", "POST"))
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        try:
            email = form.email.data
            username = form.username.data
            password = form.password.data
            
            newuser = User(
                username=username,
                email=email,
            )
            newuser.set_password(password)
            db.session.add(newuser)
            db.session.commit()
            user_profile = Profile(user_id = newuser.id,first_name = username)
            db.session.add(user_profile)
            db.session.commit()
            flash(f"Account Succesfully created", "success")
            return redirect(url_for("auth_views.login"))

        except Exception as e:
            print(e)
            pass

    return render_template("authentication/auth.html",form=form)

@auth_views.route("/login", methods=("GET", "POST"))
def login():
    form = LoginForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data.encode('utf-8')
        try:
            user = User.query.filter_by(email=email).first()
            if user and user.check_password(password):
                login_user(user)
                user.login_timestamp_update()
                flash("Login successfully!!!", "success") 
                return redirect(url_for('crud_views.home'))
            flash("Invalid Username or password!", "danger")
        except Exception as e:
            print(e)
            pass

    return render_template("authentication/auth.html",form=form)

@auth_views.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('crud_views.home'))

@auth_views.route("/change_password", methods=("GET", "POST"))
@login_required
def change_password():
    form = PasswordChangeForm()
    if form.validate_on_submit():
        user = current_user
        cur_pass = form.current_password.data
        new_pass = form.confirm_new_password.data
        if user.check_password(cur_pass.encode('utf-8')):
            if new_pass != cur_pass:
                user.set_password(new_pass)
                db.session.commit()
                flash("Password change successfully", "success")
            else:
                flash("Current password and new password must not be same!!", "danger")
        else:
            flash("Invalid current password!!", "danger")
    return render_template("authentication/change_password.html",form=form)

@auth_views.route('/reset_password',methods=["POST","GET"])
def reset_password():
    if request.method=="POST":
        email = request.form['mail']
        user = User.query.filter_by(email=email).first()

        if user:
            hashCode = ''.join(random.choices(string.ascii_letters + string.digits, k=24))
            user.hash_string = hashCode
            db.session.commit()

            msg = Message('Confirm Password Change',recipients = [email])
            msg.body = f"Hello {user.username},\nWe've received a request to reset your password. If you want to reset your password, click the link below and enter your new password\n" + request.host + url_for('auth_views.reset_password_validate',user_id=user.id,hashCode=user.hash_string)
            mail.send(msg)
            flash(f"We have sent password reset link in {email}..Please check your email and reset your password!!", "success")
        else:
            flash("Invalid email address!!", "danger")   
    return render_template("authentication/reset_password.html")


@auth_views.route("/reset_password/<int:user_id>/<string:hashCode>",methods=["GET","POST"])
def reset_password_validate(user_id,hashCode):
    user = User.query.filter_by(id = user_id,hash_string = hashCode).first()
    if user:
        form = PasswordResetForm()

        if form.validate_on_submit():
            new_pass = form.confirm_new_password.data
            user.set_password(new_pass)
            user.hash_string= None
            db.session.commit()
            flash("Password reset successfully", "success")
            logout_user()
            return redirect(url_for('auth_views.login'))
        else:
            return render_template("authentication/change_password.html",form=form)
    else:
        flash('Link is invalid or expired!!!!',"danger")
        return redirect(url_for('auth_views.reset_password'))