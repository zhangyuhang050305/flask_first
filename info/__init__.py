"""
Flask-SQLAlchemy = 专门给 Flask 封装的简化版（对 SQLAlchemy 做了包装）
Flask-SQLAlchemy = 套了一层 Flask 皮肤的 SQLAlchemy
"""
import logging
from logging.handlers import RotatingFileHandler

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import redis
from flask_session import Session
from flask_wtf.csrf import CSRFProtect, generate_csrf
from config import config_dict

# 定义redis_store变量
redis_store = None

# 定义db的变量
db = SQLAlchemy()

# 定义工厂方法
def create_app(config_name):
    app = Flask(__name__)

    # 根据传入的配置类名称，取出对应的配置类
    config = config_dict.get(config_name)

    # 调用日志方法，记录程序运行信息
    log_file(config.LEVEL_NAME)

    # 加载配置类
    app.config.from_object(config)

    # 创建SQLAlchemy对象那个，关联app
    db.init_app(app)

    # 创建redis对象
    """
    decode_responses=True：自动把 bytes 转成字符串
    r.set('name', '张三')
    print(r.get('name'))  
    不加：输出：b'张三'  → 你还要自己转字符串，很麻烦
    加：输出：'张三'  ✅ 直接用
    """
    global redis_store
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

    # 将首页蓝图，index注册到app中
    from info.modules.index import index_blue
    app.register_blueprint(index_blue)

    # 将认证蓝图passport_blue注册到app中
    from info.modules.passport import passport_blue
    app.register_blueprint(passport_blue)

    # 使用请求钩子拦截所有的请求，通过在cookie中设置csrf_token
    @app.after_request
    def after_request(resp):
        # after_request（请求处理之后），参数和操作对象都是 response（响应）
        csrf_tkoen = generate_csrf()
        # 将csrf_token设置到cookie中
        resp.set_cookie('csrf_tkoen', csrf_tkoen)
        # 返回响应
        return resp

    print(app.url_map)
    return app

def log_file(LEVEL_NAME):
    # 设置日志的记录等级，常见有四种，大小关系：DEBUG<INFO<WARNING<ERROR
    logging.basicConfig(level=LEVEL_NAME)  # 调试debug级
    # 创建日志记录器，指明日志保存的路径、每个日志文件的最大大小、保存的日志文件个数上限
    file_log_handler = RotatingFileHandler("logs/log", maxBytes=1024 * 1024 * 100, backupCount=10,encoding='utf-8')
    # 创建日志记录的格式 日志等级 输入日志信息的文件名 行数 日志信息
    formatter = logging.Formatter('%(levelname)s %(filename)s:%(lineno)d %(message)s')
    # 为刚创建的日志记录器设置日志记录格式
    file_log_handler.setFormatter(formatter)
    # 为全局的日志工具对象（flask app使用的）添加日志记录器
    logging.getLogger().addHandler(file_log_handler)