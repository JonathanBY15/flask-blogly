from models import db, User, Post, Tag, PostTag
from app import app

# Create all tables
with app.app_context():
    db.drop_all()
    db.create_all()

    # If tables aren't empty, empty them
    User.query.delete()
    Post.query.delete()
    Tag.query.delete()
    PostTag.query.delete()

    # Add users
    user1 = User(first_name='Alan', last_name='Alda')
    user2 = User(first_name='Joel', last_name='Burton')
    user3 = User(first_name='Jane', last_name='Smith')

    db.session.add_all([user1, user2, user3])
    db.session.commit()

    # Add posts
    post1 = Post(title='Post 1', content='Content for post 1', user_id=user1.id)
    post2 = Post(title='Post 2', content='Content for post 2', user_id=user2.id)
    post3 = Post(title='Post 3', content='Content for post 3', user_id=user3.id)

    db.session.add_all([post1, post2, post3])
    db.session.commit()

    # Add tags
    tag1 = Tag(name='fun')
    tag2 = Tag(name='exciting')
    tag3 = Tag(name='informative')

    db.session.add_all([tag1, tag2, tag3])
    db.session.commit()

    # Associate tags with posts
    post_tag1 = PostTag(post_id=post1.id, tag_id=tag1.id)
    post_tag2 = PostTag(post_id=post1.id, tag_id=tag2.id)
    post_tag3 = PostTag(post_id=post2.id, tag_id=tag2.id)
    post_tag4 = PostTag(post_id=post2.id, tag_id=tag3.id)
    post_tag5 = PostTag(post_id=post3.id, tag_id=tag1.id)
    post_tag6 = PostTag(post_id=post3.id, tag_id=tag3.id)

    db.session.add_all([post_tag1, post_tag2, post_tag3, post_tag4, post_tag5, post_tag6])
    db.session.commit()
