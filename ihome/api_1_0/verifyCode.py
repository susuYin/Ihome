import random

from . import api
from ihome.utils.captcha.captcha import captcha
from ihome import redis_store,db
from ihome.models import User
from ihome import Const
from flask import current_app, jsonify, make_response,request
from ihome.utils.response_code import RET
from ihome.libs.yuntongxun.SendTemplateSMS import CCP

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
        redis_store.setex("image_code_%s" % image_code_id, Const.IMAGE_CODE_REDIS_EXPIRE, text)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="保存图片验证码信息失败")
    ##返回图片
    resp = make_response(image_data)
    resp.headers["Content-Type"] = "image/jpg"
    return resp
@api.route("/sms_codes/<re(r'1[34578]\d{9}'):mobile>")
def get_sms_code(mobile):
    """获取短信验证码"""
    #获取之前先校验图片验证码是否填写正确
    image_code=request.args.get("image_code")
    image_code_id = request.args.get("image_code_id")
    #校验参数
    if not all([image_code,image_code_id]):
        return jsonify(errno=RET.PARAMERR, errmsg="参数不完整")
    try:
        real_image_code=redis_store.get("image_code_%s"%image_code_id)
        if type(real_image_code)==bytes:
            real_image_code=real_image_code.decode()
        print("image_code_%s"%image_code_id)
        print(real_image_code)
    except Exception as e:
        current_app.logger.error(e)
        return  jsonify(errno=RET.DBERR, errmsg="redis数据库错误")
    if real_image_code is None:
        #没有或者过期
        return jsonify(errno=RET.NODATA, errmsg="图片验证码失效")
    # 删除redis中的图片验证码，防止用户使用同一个图片验证码验证多次
    try:
        redis_store.delete("image_code_%s"%image_code_id)
    except Exception as e:
        current_app.logger.error(e)
    if real_image_code.lower()!=image_code.lower():
        return jsonify(errno=RET.DATAERR, errmsg="图片验证码错误")
    #判断对于这个手机号的操作，在60秒内有没有之前的记录，如果有，则认为用户操作频繁，不接受处理
    try:
        send_flag=redis_store.get("send_sms_code_%s" % mobile)
    except Exception as e:
        current_app.logger.error(e)
    else:
        if send_flag is not None:
            return jsonify(errno=RET.REQERR, errmsg="请求过于频繁，请60秒后重试")

    ##判断手机号是否存在
    try:
        user=User.query.filter_by(mobile=mobile).first()
    except Exception as e:
        current_app.logger.error(e)
    else:
        if user is not None:
            return jsonify(errno=RET.DATAEXIST, errmsg="手机号已存在")
    #生成6位随机验证码,如果没有6位，前面补0
    sms_code="%06d"%random.randint(0,999999)
    print(sms_code)
    try:
        redis_store.setex("sms_code_%s"%mobile,Const.SMS_CODE_REDIS_EXPIRE,sms_code)
        #记录是否发送过短信
        redis_store.setex("send_sms_code_%s" % mobile, Const.SEND_SMS_CODE_INTERVAL,1)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="保存短信验证码异常")
    ##发送短信
    try:
        ccp=CCP()
        result=ccp.sendTemplateSMS(mobile,[sms_code,int(Const.SMS_CODE_REDIS_EXPIRE/60)],1)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.THIRDERR, errmsg="发送异常")
    if result==0:
        return jsonify(errno=RET.OK, errmsg="发送成功")
    else:
        return jsonify(errno=RET.THIRDERR, errmsg="发送失败")


if __name__ == '__main__':
    get_image_code("gao")
    get_sms_code(13688815040)

