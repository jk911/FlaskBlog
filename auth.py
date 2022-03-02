from flask import Blueprint, render_template, request, flash, redirect
from flask_login import current_user, login_user, logout_user, login_required
from models import User

auth = Blueprint("auth", __name__)

@auth.route("/login", methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")
        user = User.query.filter_by(email=email).first()
        if user:
            if user.password == password:
                login_user(user, remember=True)
                return redirect("/home")
            flash("Email or Password is incorrect")
            return redirect("/login")
        flash("Email or Password is incorrect")
        return redirect("/login")
    return render_template("login.html")

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/login")

