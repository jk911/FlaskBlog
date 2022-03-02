from app import db
from flask_login import UserMixin
from enum import Enum as UserEnum
from datetime import datetime

class UserRole(UserEnum):
    ADMIN = 1
    USER = 2

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(400), nullable=False)
    active = db.Column(db.Boolean, default=True)
    role = db.Column(db.Enum(UserRole), default=UserRole.USER)
    posts = db.relationship("Post")

post_tag = db.Table("post_tag",
    db.Column("post_id", db.Integer, db.ForeignKey("post.id")),
    db.Column("tag_id", db.Integer, db.ForeignKey("tag.id"))
)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(400), nullable=False)
    body = db.Column(db.Text, nullable=False)
    slug = db.Column(db.String(400), nullable=False)
    time = db.Column(db.DateTime, default=datetime.now())
    tags = db.relationship("Tag", secondary="post_tag", backref=db.backref("posts"), lazy="dynamic")
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)

# db.drop_all()
# db.create_all()