from app.extensions import db, login, bcrypt
from flask_login import UserMixin
from datetime import datetime
from hashlib import md5
from flask import url_for
from datetime import datetime


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), index=True, unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password)
    
    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)
    
    @login.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}'

    def to_dict(self, include_email=False):
        data = {
            'id': self.id,
            'username': self.username,
            'last_seen': str(self.last_seen),
            'avatar': self.avatar(128)
        }
        if include_email:
            data['email'] = self.email
        return data
    
    def from_dict(self, data, new_user=False):
        for field in ['username', 'email']:
            if field in data:
                setattr(self, field, data[field])
        if new_user and 'password' in data:
            self.set_password(data['password'])


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    author = db.Column(db.String(20))
    date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    source = db.Column(db.String(250))
    view = db.Column(db.Integer)
    site = db.Column(db.String(20))
    uploader = db.Column(db.String(20))

    def __repr__(self):
        return f'<Article {self.title}>'

    def to_dict(self):
        data = {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'date': str(self.date),
            'source': self.source,
            'view': self.view,
            'site': self.site
        }
        return data
    
    def from_dict(self, data):
        for field in ['title', 'source', 'site', 'view', 'author']:
            if field in data:
                setattr(self, field, data[field])
        if getattr(self, 'view') is None:
            setattr(self, 'view', 0)
        if getattr(self, 'author') is None:
            setattr(self, 'author', '佚名')
