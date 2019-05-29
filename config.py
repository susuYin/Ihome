import redis
class Config(object):
    """配置信息"""
    DEBUG=True
    SECRET_KEY="gao123456"
    ##数据库
    SQLALCHEMY_DATABASE_URI="mysql://root:gao123456@192.168.99.100:3306/ihome"
    SQLALCHEMY_TRACK_MODIFICATIONS=True
    ###redis
    REDIS_HOST="192.168.99.100"
    REDIS_PORT=6379
    ####session配置
    SESSION_TYPE="redis"
    SESSION_REDIS=redis.StrictRedis(host=REDIS_HOST,port=REDIS_PORT)
    SESSION_USE_SIGNER=True ###使用混淆，对session_id进行隐藏
    PERMANENT_SESSION_LIFETIME=86400##有效期一天，单位s
####开发环境的配置信息
class DevConfig(Config):
    DEBUG = True
    pass
####生产环境的配置信息
class ProductConfig(Config):
    DEBUG = False
    pass
###构建名字与类的对应关系
config_map={
    "dev":DevConfig,
    "pro":ProductConfig
}
