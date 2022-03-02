from flask import Blueprint, render_template, request, redirect, flash
from app import db
from models import Post, Tag
from flask_login import login_required, current_user
from unidecode import unidecode

views = Blueprint("views", __name__)

@views.route("/")
@views.route("/home")
def home():
    keyword = request.args.get("keyword")
    page = request.args.get("page")
    if page and page.isdigit():
        page = int(page)
    else:
        page = 1
    if keyword:
        posts = Post.query.filter(Post.title.contains(keyword) | Post.body.contains(keyword))
    else:
        posts = Post.query.order_by(Post.id.desc())
    pages = posts.paginate(page=page,per_page=2)
    return render_template("home.html", pages=pages)

@views.route("/<slug>")
def detail(slug):
    posts = Post.query.filter_by(slug=slug).first_or_404()
    return render_template("detail.html", posts=posts)

@views.route("/create", methods=['GET','POST'])
@login_required
def create():
    if request.method == "POST":
        title = request.form.get("title")
        body = request.form.get("body")
        check = Post.query.filter_by(title=title).first()
        if not check:
            slug = unidecode(title.strip()).replace(" ","-")
            post = Post(title=title,body=body,slug=slug,user_id=current_user.id)
            db.session.add(post)
            db.session.commit()
            return redirect("/")
        flash("This title already exists, please put another title")
        return redirect("/create")
    return render_template("create.html")

@views.route("/<slug>/edit", methods=['GET','POST'])
@login_required
def edit(slug):
    posts = Post.query.filter_by(slug=slug).first_or_404()
    if request.method == "POST":
        title = request.form.get("title")
        body = request.form.get("body")
        posts.title = title
        posts.body = body
        db.session.commit()
        return redirect("/")
    title = posts.title
    body = posts.body
    slug = posts.slug
    return render_template("edit.html", title=title, body=body, slug=slug)

@views.route("/<slug>/delete", methods=['GET'])
@login_required
def delete(slug):
    posts = Post.query.filter_by(slug=slug).first_or_404()
    db.session.delete(posts)
    db.session.commit()
    return redirect("/")

@views.route("/tags/<id>")
def tagPost(id):
    tag = Tag.query.filter(Tag.id==id).first_or_404()
    name = tag.name
    return render_template("tag.html",tag=tag, name=name)