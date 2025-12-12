from datetime import datetime
from flask import render_template, redirect, url_for, flash, request, session
from sqlalchemy import desc
from app import db
from . import post_bp
from .forms import PostForm
from .models import Post, CategoryEnum

@post_bp.route('/', methods=['GET'])
def list_posts():
    stmt = db.select(Post).where(Post.is_active.is_(True)).order_by(desc(Post.posted))
    posts = db.session.scalars(stmt).all()
    return render_template('posts/posts.html', posts=posts)

@post_bp.route('/create', methods=['GET','POST'])
def create_post():
    form=PostForm()
    if form.validate_on_submit():
        post=Post(
            title=form.title.data,
            content=form.content.data,
            posted=form.publish_date.data,
            is_active=form.enabled.data,
            category=CategoryEnum(form.category.data),
            author=session.get("username","Anonymous")
        )
        db.session.add(post)
        db.session.commit()
        flash("Post added successfully","success")
        return redirect(url_for('posts.list_posts'))
    return render_template('posts/add_post.html', form=form, title="Add Post")

@post_bp.route('/<int:id>', methods=['GET'])
def detail_post(id):
    post=db.get_or_404(Post, id)
    return render_template('posts/detail_post.html', post=post)

@post_bp.route('/<int:id>/update', methods=['GET','POST'])
def update_post(id):
    post=db.get_or_404(Post, id)
    form=PostForm(obj=post)
    if request.method=='GET':
        form.publish_date.data=post.posted
        form.enabled.data=post.is_active
        form.category.data=post.category.value
    if form.validate_on_submit():
        post.title=form.title.data
        post.content=form.content.data
        post.is_active=form.enabled.data
        post.posted=form.publish_date.data
        post.category=CategoryEnum(form.category.data)
        db.session.commit()
        flash("Post updated","success")
        return redirect(url_for('posts.detail_post', id=post.id))
    return render_template('posts/add_post.html', form=form, title="Edit Post", is_edit=True)

@post_bp.route('/<int:id>/delete', methods=['GET','POST'])
def delete_post(id):
    post=db.get_or_404(Post, id)
    if request.method=='POST':
        db.session.delete(post)
        db.session.commit()
        flash("Post deleted","success")
        return redirect(url_for('posts.list_posts'))
    return render_template('posts/delete_confirm.html', post=post)
