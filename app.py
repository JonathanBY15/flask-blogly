"""Blogly application."""

from flask import Flask, render_template, redirect, request
from models import db, connect_db, User, Post, Tag, DEFAULT_IMAGE_URL

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:walmart48@localhost/blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'somesecretkey'

connect_db(app)

# Routes
@app.route('/')
def home():
    """Redirect to /users."""
    return redirect('/users')

@app.route('/users')
def users_list():
    """Show list of users."""
    users = User.query.all()
    return render_template('users.html', users=users)

@app.route('/users/new')
def new_user():
    """Show form to add a new user."""
    return render_template('new_user.html')

@app.route('/users/new', methods=['POST'])
def add_user():
    """Add user and redirect to /users."""
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form.get('image_url') or DEFAULT_IMAGE_URL

    new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)

    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>')
def show_user(user_id):
    """Show user details."""
    user = User.query.get_or_404(user_id)
    return render_template('user.html', user=user)

@app.route('/users/<int:user_id>/edit')
def edit_user(user_id):
    """Show form to edit a user."""
    user = User.query.get_or_404(user_id)
    return render_template('edit_user.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=['POST'])
def update_user(user_id):
    """Update user and redirect to /users."""
    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form.get('image_url') or DEFAULT_IMAGE_URL

    db.session.add(user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>/delete', methods=['POST', 'GET'])
def delete_user(user_id):
    """Delete user and redirect to /users."""
    user = User.query.get_or_404(user_id)

    db.session.delete(user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>/posts/new')
def new_post(user_id):
    """Show form to add a new post."""
    user = User.query.get_or_404(user_id)
    return render_template('new_post.html', user=user)

@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def add_post(user_id):
    """Add post and redirect to /users."""
    user = User.query.get_or_404(user_id)
    title = request.form['title']
    content = request.form['content']

    new_post = Post(title=title, content=content, user=user)

    db.session.add(new_post)
    db.session.commit()

    return redirect(f'/users/{user_id}')

@app.route('/posts/<int:post_id>')
def show_post(post_id):
    """Show post details."""
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', post=post, user=post.user)

@app.route('/posts/<int:post_id>/edit')
def edit_post(post_id):
    """Show form to edit a post."""
    post = Post.query.get_or_404(post_id)
    return render_template('edit_post.html', post=post)

@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def update_post(post_id):
    """Update post and redirect to user."""
    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']

    db.session.add(post)
    db.session.commit()

    user_id = post.user.id

    return redirect(f'/users/{user_id}')

@app.route('/posts/<int:post_id>/delete', methods=['POST', 'GET'])
def delete_post(post_id):
    """Delete post and redirect to /users."""
    post = Post.query.get_or_404(post_id)

    user_id = post.user.id

    db.session.delete(post)
    db.session.commit()

    return redirect(f'/users/{user_id}')

@app.route('/tags')
def tags_list():
    """Show list of tags."""
    tags = Tag.query.all()
    return render_template('tags.html', tags=tags)

@app.route('/tags/<int:tag_id>')
def show_tag(tag_id):
    """Show tag details."""
    tag = Tag.query.get_or_404(tag_id)
    return render_template('tag.html', tag=tag)

@app.route('/tags/new')
def new_tag():
    """Show form to add a new tag."""
    return render_template('new_tag.html')

@app.route('/tags/new', methods=['POST'])
def add_tag():
    """Add tag and redirect to /tags."""
    name = request.form['name']

    new_tag = Tag(name=name)

    db.session.add(new_tag)
    db.session.commit()

    return redirect('/tags')

@app.route('/tags/<int:tag_id>/edit')
def edit_tag(tag_id):
    """Show form to edit a tag."""
    tag = Tag.query.get_or_404(tag_id)
    return render_template('edit_tag.html', tag=tag)

@app.route('/tags/<int:tag_id>/edit', methods=['POST'])
def update_tag(tag_id):
    """Update tag and redirect to /tags."""
    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form['name']

    db.session.add(tag)
    db.session.commit()

    return redirect('/tags')

@app.route('/tags/<int:tag_id>/delete', methods=['POST', 'GET'])
def delete_tag(tag_id):
    """Delete tag and redirect to /tags."""
    tag = Tag.query.get_or_404(tag_id)

    db.session.delete(tag)
    db.session.commit()

    return redirect('/tags')