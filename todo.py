from flask import Flask, render_template, redirect,url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask.signals import message_flashed
from sqlalchemy import desc
import os
from sqlalchemy.sql.expression import true

file_path = os.path.abspath(os.getcwd())+"\db.db"
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+file_path
db = SQLAlchemy(app)
sayac=0

#Anasayfa ve listeleme
@app.route("/")
def index():
    #todos=Todo.query.all().order_by("id desc")
    todos=Todo.query.order_by(Todo.id.desc()).all()
    return render_template("index.html",todos=todos)

#Sıralama
@app.route("/sirala/alfabetik")
def siralaAlfabetik():
    global sayac
    if sayac % 2 == 0:
        todos=Todo.query.order_by(Todo.title.asc()).all()
        sayac=sayac+1
        return render_template("index.html",todos=todos)
    else:
        todos=Todo.query.order_by(Todo.title.desc()).all()
        sayac=sayac+1
        return render_template("index.html",todos=todos)

@app.route("/sirala/durum")
def siralaDurum():
    global sayac
    if sayac % 2 == 0:
        todos=Todo.query.order_by(Todo.complete.asc()).all()
        sayac=sayac+1
        return render_template("index.html",todos=todos)
    else:
        todos=Todo.query.order_by(Todo.complete.desc()).all()
        sayac=sayac+1
        return render_template("index.html",todos=todos)


@app.route("/sirala/idd")
def siralaID():
    global sayac
    if sayac % 2 == 0:
        todos=Todo.query.order_by(Todo.id.asc()).all()
        sayac=sayac+1
        return render_template("index.html",todos=todos)
    else:
        todos=Todo.query.order_by(Todo.id.desc()).all()
        sayac=sayac+1
        return render_template("index.html",todos=todos)

#Güncelle
@app.route("/complete/<string:id>")
def completeToDo(id):
    todo=Todo.query.filter_by(id=id).first()
    todo.complete= not todo.complete
    db.session.commit()
    return redirect(url_for("index"))


#Sil
@app.route("/delete/<string:id>")
def deleteToDo(id):
    todo=Todo.query.filter_by(id=id).first()
    db.session.delete(todo)
    db.session.commit()
    flash("ToDo silindi.", "danger")
    return redirect(url_for("index"))

#Ekleme
@app.route("/add", methods=["POST"])
def addTodo():
    title=request.form.get("title")
    if title=="":
        flash("ToDo boş olamaz.", "danger")
        return redirect(url_for("index"))
    else:
        newTodo=Todo(title=title,complete=False)
        db.session.add(newTodo)
        db.session.commit()
        flash("ToDo eklendi.", "success")
        return redirect(url_for("index"))

#Tablonun oluşturulması
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    complete = db.Column(db.Boolean)

app.secret_key="marfan"
if __name__=="__main__":
    db.create_all()
    app.run(debug=True)
