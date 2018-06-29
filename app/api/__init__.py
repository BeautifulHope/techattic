from flask import Blueprint
from flask_restful import Api
from app.api.users import UserResource
from app.api.articles import ArticleResource

bp = Blueprint('api', __name__)
api = Api(bp)

api.add_resource(UserResource, '/users/<int:user_id>', '/users')
api.add_resource(ArticleResource, '/articles/<int:article_id>', '/articles')