"""
相关配置
1.数据库配置：为了在项目中用来存储新闻数据以及用户数据的
2.redis配置：缓存访问频率高的内容，存储session信息，图片验证码，短信验证码
3.session配置:将来用来保存用户的登录信息
4.csrf配置:保护app，防止csrf攻击
校验的请求方式：POST,PUT,DELETE,PATCH
会修改数据（危险请求）→ 必须校验 CSRF
"""
from datetime import timedelta

"""
Flask-SQLAlchemy = 专门给 Flask 封装的简化版（对 SQLAlchemy 做了包装）
Flask-SQLAlchemy = 套了一层 Flask 皮肤的 SQLAlchemy
"""
from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
import redis
from flask_session import Session
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)

# 设置配置信息
class Config:
    # 调试级别
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


app.config.from_object(Config)

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
    host=Config.REDIS_HOST,
    port=Config.REDIS_PORT,
    decode_responses=True,
    db=0
)

# 创建Session对象，读取APP中session配置信息
Session(app)

# 使用csrfprotect保护app
CSRFProtect(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    # 测试redis存取数据
    redis_store.set('name','laowang')
    print(redis_store.get('name'))

    # 测试session存取
    session['name'] = 'zhangsan'
    print(session.get('name'))

    return 'hello world'

if __name__ == '__main__':
    app.run()