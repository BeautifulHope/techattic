from flask_restful import Resource, abort
from app.models import Article
from flask import request
from app.extensions import db


class ArticleResource(Resource):
    def get(self, article_id):
        article = Article.query.get(article_id)
        return article.to_dict() if article else abort(404, message='This article does not exist.')
    
    def post(self):
        data = request.get_json() or {}
        if not all(field in data for field in ['title', 'source', 'site']):
            abort(400, message='You must have 3 fields: title, source and site.')
        if Article.query.filter_by(title=data['source']).first():
            abort(400, message='This article already exists!')
        article = Article()
        article.from_dict(data)
        db.session.add(article)
        db.session.commit()
        return article.to_dict(), 201
