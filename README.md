# Techattic

一家利用[爬虫技术](https://github.com/alphardex/blogcrawler)将众多IT技术博客站点集成于一站的网站。

**注意：本网站仅充当一个技术文章的搜索引擎（通俗点讲是桥梁），和文章的版权毫无半点关系。**

项目demo地址：[猛戳这里](http://techattic.herokuapp.com/)

## 架构

- Flask
- Scrapy

## 开发流程

### 网站搭建

把项目下载到本地

``` bash
git clone https://github.com/alphardex/techattic.git
```

创建虚拟环境并安装依赖

``` bash
python -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt
```

运行app即可

``` bash
export FLASK_APP=techattic.py
flask run
```

### 数据库搭建

在MySQL中创建db

``` sql
CREATE USER 'test'@'localhost' IDENTIFIED BY 'test123';
GRANT ALL PRIVILEGES ON *.* TO 'test'@'localhost';
FLUSH PRIVILEGES;
CREATE DATABASE techattic DEFAULT CHARACTER SET utf8 COLLATE utf8_bin;
```

用爬虫获取数据

``` bash
cd crawler
python fetchall.py
```

最后迁移数据库，完成！

``` bash
flask db migrate
flask db upgrade
```