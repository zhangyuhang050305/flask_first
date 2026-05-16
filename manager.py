"""
相关配置
1.数据库配置：为了在项目中用来存储新闻数据以及用户数据的
2.redis配置：缓存访问频率高的内容，存储session信息，图片验证码，短信验证码
3.session配置
4.csrf配置
"""

from flask import Flask
from flask_sqlalchemy import SQLALchemy, SQLAlchemy

app = Flask(__name__)

# 设置配置信息
class Config:
    # 调试级别
    DEBUG = True

    # 数据库配置信息
    DATABASE_URI = 'mysql+pymysql://root:123456@localhost:3306/info36?charset=utf8mb4'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

app.config.from_object(Config)

# 创建SQLAlchemy对象那个，关联app
db = SQLAlchemy(app)
@app.route('/')
def index():
    return 'hello world'

if __name__ == '__main__':
    app.run()