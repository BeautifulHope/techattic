from flask import render_template, redirect, url_for, flash, request, abort
from app.auth.forms import LoginForm, RegisterForm
from app.auth import bp
from flask_login import current_user, login_user, logout_user
from app.models import User
from app.extensions import db
from urllib.parse import urlparse, urljoin
from flask_babel import _


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        login_user(user, remember=form.remember_me.data)
        flash(_('登录成功！'), 'success')
        return redirect(request.args.get('next') or url_for('main.index'))
    return render_template('auth/login.html', form=form)


@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(_('注册成功！'), 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)


@bp.route('/logout')
def log_out():
    logout_user()
    return redirect(url_for('main.index'))
