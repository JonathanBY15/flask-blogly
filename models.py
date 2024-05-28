from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

DEFAULT_IMAGE_URL = "https://cdn-icons-png.flaticon.com/128/1077/1077063.png"

class User(db.Model):
    """User."""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    image_url = db.Column(db.String(500), nullable=True, default=DEFAULT_IMAGE_URL)

class Post(db.Model):
    """Post."""

    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50), nullable=False)
    content = db.Column(db.String(500), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    user = db.relationship('User', backref='posts')

def connect_db(app):
    """Connect db to flask."""

    db.app = app
    db.init_app(app)