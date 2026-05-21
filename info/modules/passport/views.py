import json
import re

from . import passport_blue
from ...utils.captcha.captcha import captcha
from flask import request, current_app, make_response, jsonify
from info import redis_store,constants
from info.sms import CCP

# 功能：获取图片验证码
# 请求路径：/passport/image_code
# 请求方式：GET
# 请求参数：cur_id,pre_id
# 返回值：图片验证码
@passport_blue.route('/image_code', )
def image_code():
    # 1.获取前端传递的参数
    cur_id = request.args.get("cur_id")
    pre_id = request.args.get("pre_id")

    # 2.调用gennerate_captcha获取图片验证码编号，验证码值，图片(二进制)
    name, text, image_data = captcha.generate_captcha()

    try:
        # 3.将图片验证码的值保存在redis
        redis_store.setex("image_code:%s"%cur_id,constants.IMAGE_CODE_REDIS_EXPIRES,text)

        # 4.判断是否有上一次的图片验证
        if pre_id:
            redis_store.delete("image_code:%s"%pre_id)
    except Exception as e:
        current_app.logger.error(e)
        return "图片验证码操作失败"

    # 返回图片
    response = make_response(image_data)
    response.headers["Content-Type"] = "image/png"
    return response

# 获取短信验证码
# 请求路径：/passport/sms_code
# 请求方式：POST
# 请求参数：mobile,image_code,image_code_id
# 返回值：errno,errmsg
@passport_blue.route('/sms_code', methods=['POST'])
def sms_code():
    # 1.获取参数
    json_data = request.data
    dict_data = json.loads(json_data)
    mobile = dict_data.get("mobile")
    image_code = dict_data.get("image_code")
    image_code_id = dict_data.get("image_code_id")

    # 2.校验参数，图片验证码
    # 从redis读取图片验证码
    redis_image_code = redis_store.get("image_code:%s"%image_code_id)

    # 和传递的图片验证码比较
    if image_code != redis_image_code:
        return jsonify(errno=1000,errmsg="图片验证码错误")

    # 3.校验参数，手机格式
    if not re.match(r"1[3-9]\d{9}",mobile):
        return jsonify(errno=2000,errmsg="手机号格式错误")

    # 4.发送短信,调用分装好的cpp
    ccp = CCP()
    result = ccp.send_message('1', '18828698516', ('1234','4'))
    if result == -1:
        return jsonify(errno=3000,errmsg="短信发送失败")

    # 5.返回发送的状态
    return jsonify(errno=0,errmsg="短信发送成功")
