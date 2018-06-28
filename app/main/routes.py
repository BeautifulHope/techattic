from app.main import bp
from flask import render_template, g, request, current_app
from flask_login import login_required, current_user
from app.models import User, db, Article
from datetime import datetime
from flask_babel import get_locale
from app.main.forms import SearchForm
from sqlalchemy.sql.expression import func


@bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
        g.search_form = SearchForm()
    g.locale = str(get_locale())
    if g.locale.startswith('zh'):
        g.locale += '-cn'


@bp.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    pagination = Article.query.paginate(page, per_page=current_app.config['ARTICLE_PER_PAGE'])
    articles = pagination.items
    return render_template('index.html', pagination=pagination, articles=articles)


@bp.route('/about')
def about():
    return render_template('about.html')


@bp.route('/user/<string:username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)


@bp.route('/search')
@login_required
def search():
    q = g.search_form.q.data
    page = request.args.get('page', 1, type=int)
    pagination = Article.query.filter(Article.title.ilike(f'%{q}%')).paginate(page, per_page=current_app.config['ARTICLE_PER_PAGE'])
    articles = pagination.items
    return render_template('index.html', pagination=pagination, articles=articles)


@bp.route('/random')
def random():
    random_articles = Article.query.order_by(func.random()).limit(current_app.config['ARTICLE_PER_PAGE']).all()
    return render_template('index.html', articles=random_articles)