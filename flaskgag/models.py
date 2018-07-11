from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from flaskgag import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)  # Post Author relationship

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')


    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    post_image_file = db.Column(db.String(20), nullable=False)
    content = db.Column(db.Text, nullable=True)
    votes = db.Column(db.Integer, nullable=True, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Post Author relationship
    comments = db.relationship('Comment', backref='title', lazy='dynamic')

    def get_comments(self):
        return Comment.query.filter_by(post_id=post.id).order_by(Comment.timestamp.desc())


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))

    def __repr__(self):
        return '<Post %r>' % self.body


class Vote(db.Model):
    vote_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=True)
    post_id = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return f"Vote('{self.user_id}', '{self.post_id}')"


'''
from flaskgag import create_app
from flaskgag import db
from flaskgag.models import current_app, User, Post, Vote, Comment
app = create_app()
app.app_context().push()
print (app)

# Now you can run queries against your database.
User.query.all()
Post.query.all()
Vote.query.all()
db.create_all()
'''