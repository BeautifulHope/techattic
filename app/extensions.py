from flask_bootstrap import Bootstrap
from flask_debugtoolbar import DebugToolbarExtension
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_moment import Moment
from flask_babel import Babel, lazy_gettext as _l


bootstrap = Bootstrap()
debugtoolbar = DebugToolbarExtension()
db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'
login.login_message = _l('对不起，您还没有登录！')
login.login_message_category = 'danger'
moment = Moment()
babel = Babel()
