# flask-sample
[![Build Status](https://travis-ci.org/alphardex/flask-sample.svg?branch=master)](https://travis-ci.org/alphardex/flask-sample)

这是flask的项目示范，可以把它当做flask开发的绝佳模板。

## 项目特征

- 前端美化：[Flask-Bootstrap](https://pythonhosted.org/Flask-Bootstrap/)
- 表单：[Flask-WTF](https://flask-wtf.readthedocs.io/)
- 数据库：[Flask-SQLAlchemy](http://flask-sqlalchemy.pocoo.org/2.3/)+[Flask-Migrate](https://github.com/miguelgrinberg/Flask-Migrate)（User Model）
- 登录注册：[Flask-Login](https://flask-login.readthedocs.io/)
- 密码哈希：[Flask-Bcrypt](https://github.com/maxcountryman/flask-bcrypt)
- 时间支持: [Flask-Moment](https://github.com/miguelgrinberg/Flask-Moment)
- 国际化: [Flask-Babel](https://pythonhosted.org/Flask-Babel/)
- DEBUG: [Flask-Debugtoolbar](https://github.com/mgood/flask-debugtoolbar)
- API: [Flask-Restful](http://flask-restful.readthedocs.io/en/latest/)
- 后台: [Flask-Admin](https://flask-admin.readthedocs.io/en/latest/)
- 最佳实践：[Blueprints](http://flask.pocoo.org/docs/1.0/blueprints/)以及[工厂模式](http://flask.pocoo.org/docs/1.0/patterns/appfactories)
- 代码整齐精炼

## 开发流程

把项目下载到本地

``` bash
git clone https://github.com/alphardex/flask-sample.git
```

创建虚拟环境并安装依赖

``` bash
python -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt
```

运行app即可

``` bash
export FLASK_APP=flask-sample.py
flask run
```