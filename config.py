import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'f43hrt53et53'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or ('mysql+pymysql://test:test123@localhost/techattic?charset=utf8mb4')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    LANGUAGES = ['zh', 'en', 'ja']
    BABEL_DEFAULT_LOCALE = 'zh'
    ARTICLE_PER_PAGE = 20
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')