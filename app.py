"""Blogly application."""

from flask import Flask, render_template, redirect, request
from models import db, connect_db, User, DEFAULT_IMAGE_URL

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