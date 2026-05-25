import logging
from flask import current_app, render_template, session

from info import redis_store
from info.modules.index import index_blue
from info.models import User

@index_blue.route('/',methods=['GET','POST'])
def index():
    # 1.获取用户的登录信息
    user_id = session.get('user_id')

    # 2.通过user_id取出用户的对象
    user =None
    if user_id:
        try:
            user = User.query.get(user_id)
        except Exception as e:
            current_app.logger.error(e)

    # 3.拼接用户数据，渲染页面
    data = {
        "user_info":user.to_dict() if user else None
    }
    return render_template("news/index.html",data=data)


# 处理网站logo
@index_blue.route('/favicon.ico')
def get_web_logo():
    return current_app.send_static_file('news/favicon.ico')