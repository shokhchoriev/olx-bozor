from flask import Flask, render_template, redirect, session, url_for, \
    request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.utils import secure_filename
from sqlalchemy.orm import relationship
import os


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.secret_key = "test"
db = SQLAlchemy(app)


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(20), unique=True, nullable=False)
    parol = db.Column(db.String(50), nullable=False)
    date_joined = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"User: {self.name}"
    
class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    info = db.Column(db.Text, default="")
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    image_url = db.Column(db.String(100), default="rasmlar/default.png")
    price = db.Column(db.Integer, default=0)
    status = db.Column(db.Boolean, default=True)
    sold = db.Column(db.Boolean, default=False)
    user = relationship("Users", backref="posts")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"Post: {self.title} | {self.user.name}"


@app.route("/")
def index():
    name = session.get("name")
    if name is None:
        return redirect(url_for("login"))
    return render_template("index.html", name=name)


@app.route("/login", methods=['GET', "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        phone_number = request.form.get("phone")
        password = request.form.get("parol")
        user = Users.query.filter_by(
            phone_number=phone_number,
            parol=password
        ).first()
        if user:
            session['name'] = user.name
            session['user_id'] = user.id
            return redirect(url_for('index'))
        return redirect(url_for('login'))


@app.route("/register", methods=['GET', "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        name = request.form.get("ism")
        phone_number = request.form.get("phone")
        password = request.form.get("parol")
        try:
            user = Users(
                name=name,
                phone_number=phone_number,
                parol=password
            )
            db.session.add(user)
            db.session.commit()
            session['name'] = user.name
            session['user_id'] = user.id
            return redirect(url_for('index'))
        except:
            return redirect(url_for(request.url))


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('login'))





if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
