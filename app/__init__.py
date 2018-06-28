from flask import Flask, request, current_app, g
from config import Config
from app.extensions import *
from flask_admin.contrib.sqla import ModelView
from app.models import User, Article


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    bootstrap.init_app(app)
    debugtoolbar.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    bcrypt.init_app(app)
    moment.init_app(app)
    babel.init_app(app)
    admin.init_app(app)

    if not app.config['TESTING']:
        # Avoiding name collision between blueprints
        admin.add_view(ModelView(User, db.session))
        admin.add_view(ModelView(Article, db.session))

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    return app

@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(current_app.config['LANGUAGES'])

from app import models