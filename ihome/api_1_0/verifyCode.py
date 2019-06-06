from . import api
from ihome.utils.captcha.captcha import captcha
from ihome import redis_store
from ihome import Const
from flask import current_app, jsonify, make_response
from ihome.utils.response_code import RET


@api.route("/images_codes/<image_code_id>")
def get_image_code(image_code_id):
    ##获取图片验证码 返回值：验证码图片
    ##获取参数、检验参数、业务逻辑处理、返回值
    ##生成验证码图片，保存验证码真实值和编号到redis，返回图片
    name, text, image_data = captcha.generate_captcha()
    # redis_store.set("img_code_%s" % image_code_id,text)
    # redis_store.expire("img_code_%s" % image_code_id,Const.IMAGE_CODE_REDIS_EXPIRE)
    # 上面两句可整合成下面一句，同时设置值和有效期
    # 连接终端，异常处理
    try:
        redis_store.setex("img_code_%s" % image_code_id, Const.IMAGE_CODE_REDIS_EXPIRE, text)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="保存图片验证码信息失败")
    ##返回图片
    resp = make_response(image_data)
    resp.headers["Content-Type"] = "image/jpg"
    return resp





