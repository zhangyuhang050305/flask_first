from flask import current_app, jsonify, render_template, abort

from . import news_blue
from ...models import News
from ...utils.response_code import RET

# 请求路径：/news/<int:news_id>
# 请求方式：GET
# 请求参数
# 返回值
@news_blue.route("/<int:news_id>")
def news_id(news_id):
    # 1.根据新闻编号，查询新闻对象
    try:
        news = News.query.get(news_id)
    except Exception as e:
        current_app.logger.errno(e)
        return jsonify(errno=RET.DBERR,errmsg="获取新闻失败")

    # 2.如果新闻不存在直接抛出异常
    if not news:
        abort(404)

    # 2.携带数据，渲染页面
    data = {
        "news_info": news.to_dict()
    }

    return render_template("news/detail.html", data=data)