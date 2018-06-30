from app.main import bp
from flask import render_template, g, request, current_app, make_response, flash, redirect, url_for
from flask_login import login_required, current_user
from app.models import User, db, Article
from datetime import datetime
from flask_babel import get_locale
from app.main.forms import SearchForm, UploadForm
from sqlalchemy.sql.expression import func
from werkzeug.urls import url_encode
from flask_babel import _


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
    article_query = get_sorted_article_query()
    pagination = article_query.paginate(page, per_page=current_app.config['ARTICLE_PER_PAGE'])
    articles = pagination.items
    return render_template('index.html', pagination=pagination, articles=articles, can_sort=True)


@bp.route('/about')
def about():
    return render_template('about.html')


@bp.route('/user/<string:username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    pagination = Article.query.filter_by(uploader=username).paginate(page, per_page=current_app.config['ARTICLE_PER_PAGE'])
    uploaded_articles = pagination.items
    return render_template('user.html', user=user, articles=uploaded_articles, can_sort=False)


@bp.route('/search')
def search():
    q = g.search_form.q.data
    page = request.args.get('page', 1, type=int)
    article_query = get_sorted_article_query()
    pagination = article_query.filter(Article.title.ilike(f'%{q}%')).paginate(page, per_page=current_app.config['ARTICLE_PER_PAGE'])
    articles = pagination.items
    return render_template('index.html', pagination=pagination, articles=articles, can_sort=True)


@bp.route('/random')
def random():
    random_articles = Article.query.order_by(func.random()).limit(current_app.config['ARTICLE_PER_PAGE']).all()
    return render_template('index.html', articles=random_articles, can_sort=False)


@bp.route('/<string:field>/<string:value>')
def search_by_field(field, value):
    page = request.args.get('page', 1, type=int)
    article_query = get_sorted_article_query()
    filtered_query = None
    if field == 'author':
        filtered_query = article_query.filter_by(author=value)
    elif field == 'site':
        filtered_query = article_query.filter_by(site=value)
    else:
        filtered_query = article_query
    pagination = filtered_query.paginate(page, per_page=current_app.config['ARTICLE_PER_PAGE'])
    articles = pagination.items
    return render_template('index.html', pagination=pagination, articles=articles, can_sort=True)


@bp.route('/rss')
def rss():
    articles = Article.query.limit(10)
    rss = render_template('rss.xml', articles=articles)
    response = make_response(rss)
    response.headers['Content-Type'] = 'application/xml'
    return response


@bp.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    form = UploadForm()
    if form.validate_on_submit():
        article = Article(title=form.title.data, source=form.source.data, author=form.author.data, site=form.site.data, uploader=current_user.username)
        db.session.add(article)
        db.session.commit()
        flash(_('发表成功！'), 'success')
        return redirect(url_for('main.index'))
    return render_template('upload.html', form=form)


@bp.app_template_global()
def append_query(**new_values):
    """Add new querystring based on the original querystring.

    Returns:
        str: url with a new querystring
    """
    args = request.args.copy()
    for k, v in new_values.items():
        args[k] = v
    return f'{request.path}?{url_encode(args)}'


@bp.app_template_global()
def get_sorted_article_query():
    """Get sorted query object of article. Judging by its sort_key and order.
    
    Returns:
        object: Article.query (sorted)
    """
    sort_key = request.args.get('s')
    order = request.args.get('o')
    article_query = None
    if sort_key:
        if order == 'asc':
            article_query = Article.query.order_by(db.asc(sort_key))
        else:
            article_query = Article.query.order_by(db.desc(sort_key))
    else:
        article_query = Article.query
    return article_query

