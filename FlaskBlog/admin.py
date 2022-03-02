from flask_admin import expose, BaseView
from flask_login import current_user, logout_user
from flask import redirect
from flask_admin.contrib.sqla import ModelView

class PostModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated

class UserModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated

class TagModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated

class LogoutView(BaseView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect("/admin")
    def is_accessible(self):
        return current_user.is_authenticated