import redis
from datetime import timedelta

# 设置配置信息（基类配置信息）
class Config:
    # 调试信息
    DEBUG = True
    SECRET_KEY = 'sdfsdfefcxcfdf'

    # 数据库配置信息
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@localhost:3306/info36?charset=utf8mb4'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # redis配置信息
    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = 6379

    # session配置信息
    SESSION_TYPE = 'redis' # 设置session存储类型
    SESSION_REDIS = redis.Redis(host=REDIS_HOST,port=REDIS_PORT) #只当session存储的redis服务器
    SESSION_USE_SIGNER = True #设置签名存储
    PERMANENT_SESSION_LIFETIME = timedelta(days=5) # 设置session的有效期

# 开发环境配置信息
class DevelopConfig(Config):
    pass

# 生产（线上）环境配置信息
class ProductConfig(Config):
    DEBUG = False

# 测试环境配置信息
class TestConfig(Config):
    pass

# 提供一个统一的访问入口
config_dict = {
    'development': DevelopConfig,
    'production': ProductConfig,
    'test': TestConfig
}