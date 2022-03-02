from flask import Flask, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_admin import Admin

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root@localhost/test"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["SECRET_KEY"] = "just for fun"
db = SQLAlchemy(app)
admin = Admin(app, name="Management System", template_mode="bootstrap4")

@app.errorhandler(404)
def pageNotfound(e):
    return render_template("404.html")

login_manager = LoginManager()
login_manager.login_view = "/login"
login_manager.init_app(app)
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

if __name__ == "__main__":
    from views import views
    from auth import auth
    from models import User, Post, Tag
    from admin import *
    admin.add_view(PostModelView(Post, db.session))
    admin.add_view(TagModelView(Tag, db.session))
    admin.add_view(UserModelView(User, db.session))
    admin.add_view(LogoutView(name="Logout"))
    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")
    app.run(debug=True)