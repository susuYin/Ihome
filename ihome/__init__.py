#coding=utf-8
import redis
from flask import Flask
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from config import config_map, Config
from ihome import api_1_0

##创建db对象，app创建出来之后自动绑定
db=SQLAlchemy()
#创建redis连接对象
redis_store=None
#工厂模式创建app对象
def creat_app(config_name):
    """创建flask应用对象
    :param config_name:str 配置模式的名字
    :return：
    """
    app = Flask(__name__)
    config_class=config_map.get(config_name)
    ###根据配置模式的名字获取配置参数的类
    app.config.from_object(config_class)
    ##使用appdb
    db.init_app(app)
    global redis_store
    redis_store = redis.StrictRedis(host=config_class.REDIS_HOST, port=config_class.REDIS_PORT)
    ##将session数据保存到redis
    Session(app)
    ##添加CSRF防护机制
    CSRFProtect(app)
    ###注册蓝图
    app.register_blueprint(api_1_0.api,url_prefix="/api/V1.0")

    return app
