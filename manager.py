"""
Flask-SQLAlchemy = 专门给 Flask 封装的简化版（对 SQLAlchemy 做了包装）
Flask-SQLAlchemy = 套了一层 Flask 皮肤的 SQLAlchemy
"""
from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
import redis
from flask_session import Session
from flask_wtf.csrf import CSRFProtect
from config import Config

app = Flask(__name__)

# 加载配置类
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