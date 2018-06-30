import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, request, current_app, g
from config import Config
from app.extensions import *
from app.models import User, Article


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    bootstrap.init_app(app)
    debugtoolbar.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    moment.init_app(app)
    babel.init_app(app)
    
    if not app.debug and not app.testing:
        if app.config['LOG_TO_STDOUT']:
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(logging.INFO)
            app.logger.addHandler(stream_handler)
        else:
            if not os.path.exists('logs'):
                os.mkdir('logs')
            file_handler = RotatingFileHandler('logs/techattic.log', maxBytes=10240, backupCount=10)
            file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s ''[in %(pathname)s:%(lineno)d]'))
            file_handler.setLevel(logging.INFO)
            app.logger.addHandler(file_handler)

            app.logger.setLevel(logging.INFO)
            app.logger.info('Techattic startup')


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