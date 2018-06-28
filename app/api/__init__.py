from flask import Blueprint
from flask_restful import Api
from app.api.users import UserResource

bp = Blueprint('api', __name__)
api = Api(bp)

api.add_resource(UserResource, '/users/<int:user_id>')