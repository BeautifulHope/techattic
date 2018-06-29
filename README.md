# Techattic

一家利用爬虫技术将众多IT技术博客站点集成于一站的网站。
注意：本网站仅充当一个技术文章的搜索引擎（通俗点讲是桥梁），和文章的版权毫无半点关系。

## 架构

- flask
- Scrapy

## 开发流程

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