from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from app.models import User
from flask_babel import _, lazy_gettext as _l


class LoginForm(FlaskForm):
    username = StringField(_l('用户名'), validators=[DataRequired()])
    password = PasswordField(_l('密码'), validators=[DataRequired()])
    remember_me = BooleanField(_l('记住我'))
    submit = SubmitField(_l('登录'))

    def validate(self):
        initial_validation = super(LoginForm, self).validate()
        if not initial_validation:
            return False

        self.user = User.query.filter_by(username=self.username.data).first()

        if not self.user:
            self.username.errors.append('该用户不存在！')
            return False

        if not self.user.check_password(password=self.password.data):
            self.password.errors.append('密码错误！')
            return False
        return True


class RegisterForm(FlaskForm):
    username = StringField(_l('用户名'), validators=[DataRequired()])
    email = StringField(_l('邮箱'), validators=[Email(), DataRequired()])
    password = PasswordField(_l('密码'), validators=[DataRequired()])
    confirm = PasswordField(_l('确认密码'), validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField(_l('注册'))

    def validate(self):
        initial_validation = super(RegisterForm, self).validate()
        if not initial_validation:
            return False

        self.user = User.query.filter_by(username=self.username.data).first()
        self.email_ = User.query.filter_by(email=self.email.data).first()

        if self.user:
            self.username.errors.append('该用户已存在！')
            return False

        if self.email_:
            self.email.errors.append('该邮箱已存在！')
            return False
        return True