from flask import flash, redirect, render_template, request,Blueprint
from .models import ToDoInfo
from crud import db
from flask_login import login_required


crud_views = Blueprint('crud_views', __name__)

@crud_views.route('/')
def home():
    user_data = ToDoInfo.query.all()
    return render_template('crud/home.html',user_data=user_data)

@crud_views.route('/create',methods=["POST"])
@login_required
def create():
    tl = request.form.get('title')
    ds = request.form.get('description')

    if tl != '' and ds != '':
        try:
            todo_info = ToDoInfo(title=tl, description=ds)
            db.session.add(todo_info)
            db.session.commit()
            flash("Data submited successfully!!", "success")
        except Exception as e:
            print(e)
            flash("Title or description already exist!!!", "danger")
        return redirect('/')
    else:
        flash("Title or description may not blank!!!", "danger")
        return redirect('/')

@crud_views.route('/edit/<int:id>',methods=["GET",'POST'])
@login_required
def edit(id):
    todo_info = ToDoInfo.query.get(id)
    if request.method == 'POST':
        tl = request.form.get('title')
        ds = request.form.get('description')
        todo_info.title=tl
        todo_info.description=ds
        db.session.commit()
        flash("Data updated successfully!!", "success")
        return redirect('/')
    else:
        if todo_info is None:
            flash("Data Not found!!", "danger")
            return redirect('/')
        return render_template('crud/edit.html',data=todo_info)

@crud_views.route('/delete/<int:id>',methods=["GET"])
@login_required
def delete(id):
    todo_info = ToDoInfo.query.get(id)
    if todo_info is None:
        flash("Data Not found!!", "danger")
        return redirect('/')
    else:
        db.session.delete(todo_info)
        db.session.commit()
        flash("Data deleted successfully!!", "success")
        return redirect('/')