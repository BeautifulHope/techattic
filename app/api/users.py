from flask_restful import Resource, abort
from app.models import User
from flask import request
from app.extensions import db


class UserResource(Resource):
    def get(self, user_id):
        user = User.query.get(user_id)
        return user.to_dict() if user else abort(404, message='This user does not exist.')
    
    def post(self):
        data = request.get_json() or {}
        if not all(field in data for field in ['username', 'email', 'password']):
            abort(400, message='You must have 3 fields: username, email and password.')
        if User.query.filter_by(username=data['username']).first():
            abort(400, message='User already exists!')
        if User.query.filter_by(email=data['email']).first():
            abort(400, message='Email already exists!')
        user = User()
        user.from_dict(data, new_user=True)
        db.session.add(user)
        db.session.commit()
        return user.to_dict(), 201
    
    def put(self, user_id):
        user = User.query.get(user_id)
        if not user:
            abort(404, message='This user does not exist.')
        data = request.get_json() or {}
        if 'username' in data and User.query.filter_by(username=data['username']).first():
            abort(400, message='Username already exists!')
        if 'email' in data and User.query.filter_by(email=data['email']).first():
            abort(400, message='Email already exists!')
        user.from_dict(data)
        db.session.commit()
        return user.to_dict()