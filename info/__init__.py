"""
Flask-SQLAlchemy = 专门给 Flask 封装的简化版（对 SQLAlchemy 做了包装）
Flask-SQLAlchemy = 套了一层 Flask 皮肤的 SQLAlchemy
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import redis
from flask_session import Session
from flask_wtf.csrf import CSRFProtect
from config import config_dict

# 定义工厂方法
def create_app(config_name):
    app = Flask(__name__)

    # 根据传入的配置类名称，取出对应的配置类
    config = config_dict.get(config_name)

    # 加载配置类
    app.config.from_object(config)

    # 创建SQLAlchemy对象那个，关联app
    db = SQLAlchemy(app)

    # 创建redis对象
    """
    decode_responses=True：自动把 bytes 转成字符串
    r.set('name', '张三')
    print(r.get('name'))  
    不加：输出：b'张三'  → 你还要自己转字符串，很麻烦
    加：输出：'张三'  ✅ 直接用
    """
    redis_store = redis.Redis(
        host=config.REDIS_HOST,
        port=config.REDIS_PORT,
        decode_responses=True,
        db=0
    )

    # 创建Session对象，读取APP中session配置信息
    Session(app)

    # 使用csrfprotect保护app
    CSRFProtect(app)

    return app