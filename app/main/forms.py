from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_babel import _, lazy_gettext as _l
from flask import request
from app.models import Article


class SearchForm(FlaskForm):
    q = StringField(_l('搜索文章'), validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        if 'formdata' not in kwargs:
            kwargs['formdata'] = request.args
        if 'csrf_enabled' not in kwargs:
            kwargs['csrf_enabled'] = False
        super(SearchForm, self).__init__(*args, **kwargs)


class UploadForm(FlaskForm):
    title = StringField(_l('标题'), validators=[DataRequired()])
    source = StringField(_l('链接'), validators=[DataRequired()])
    author = StringField(_l('作者'))
    site = StringField(_l('站点'), validators=[DataRequired()])
    submit = SubmitField(_l('提交'))

    def validate(self):
        initial_validation = super(UploadForm, self).validate()
        if not initial_validation:
            return False
        
        self.article = Article.query.filter_by(source=self.source.data).first()
        print(self.article)

        if self.article:
            self.source.errors.append('不要上传重复的文章！')
            return False
        return True
