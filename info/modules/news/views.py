from flask import current_app, jsonify, render_template, abort, session, g

from . import news_blue
from ...models import News, User
from ...utils.commons import user_login_data
from ...utils.response_code import RET

# 请求路径：/news/<int:news_id>
# 请求方式：GET
# 请求参数
# 返回值
@news_blue.route("/<int:news_id>")
@user_login_data
def news_id(news_id):
    # # 0.从session中取出用户对象
    # user_id = session.get("user_id")
    #
    # # 0.1通过user_i取出用户对象
    # user = None
    # if user_id:
    #     try:
    #         user = User.query.get(user_id)
    #     except Exception as e:
    #         current_app.logger.error(e)

    # 1.根据新闻编号，查询新闻对象
    try:
        news = News.query.get(news_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR,errmsg="获取新闻失败")

    # 2.如果新闻不存在直接抛出异常
    if not news:
        abort(404)

    # 3.获取前6条热门新闻
    try:
        click_news = News.query.order_by(News.clicks.desc()).limit(6).all()
    except Exception as e:
        current_app.logger.error(e)
        click_news = []

    # 4.将热门新闻的对象列表，转换成字典列表
    click_news_list = []
    for hot_news in click_news:
        click_news_list.append(hot_news.to_dict())

    # 2.携带数据，渲染页面
    data = {
        "news_info": news.to_dict(),
        "user_info": g.user.to_dict() if g.user else "",
        "news_list": click_news_list
    }

    return render_template("news/detail.html", data=data)