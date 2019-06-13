import json
import re

from flask import request, jsonify, current_app, session
from sqlalchemy.exc import IntegrityError
from ihome import redis_store, db, Const
from ihome.models import User
from ihome.utils.response_code import RET
from . import api
@api.route("/users",methods=["POST"])
def register():
    #获取请求的数据，返回字典
    req_dict=request.get_json
    #req_dict('mobile')拿到的是整个json串
    req_dict=req_dict('mobile')
    mobile=req_dict['mobile']
    sms_code = req_dict["sms_code"]
    password = req_dict["password"]
    password2 = req_dict["password2"]
    #校验参数
    if not all([mobile,sms_code,password,password2]):
        return jsonify(error=RET.PARAMERR,errmsg="参数不完整")
    if not re.match(r"1[34578]\d{9}",str(mobile)):
        return jsonify(error=RET.PARAMERR,errmsg="手机号格式不正确")
    if password !=password2:
        return jsonify(error=RET.PARAMERR,errmsg="两次密码输入不一致")
    try:
        #redis的是bytes类型，需要decode成str
        real_sms_code=(redis_store.get("sms_code_%s"%mobile)).decode()
        print("real_sms_code",real_sms_code)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(error=RET.DATAERR,errmsg="读取短信验证码异常")
    if real_sms_code is None:
        return jsonify(error=RET.NODATA, errmsg="短信验证码失效")
    try:
        redis_store.delete("sms_code_%s"%mobile)
    except Exception as e:
        current_app.logger.error(e)
    if sms_code!=real_sms_code:
        return jsonify(error=RET.DATAERR, errmsg="短信验证码错误")
    ##判断用户手机号是否注册过--在下发保存时校验，表字段加了唯一索引
    # try:
    #     user=User.query.filter_by(mobile).first()
    # except Exception as e:
    #     current_app.logger.error(e)
    #     return jsonify(error=RET.DATAERR, errmsg="数据库连接错误")
    # if user is not None:
    #     return jsonify(errno=RET.DATAEXIST, errmsg="手机号已存在")
     #保存用户的注册信息到数据库
    user=User(name=mobile,mobile=mobile)
    user.password = password  # 设置属性
    #在user类通过属性函数进行加密并且保存
    #user.generate_password_hash(password)
    try:
        db.session.add(user)
        db.session.commit()
    except IntegrityError as e:
        # 数据库操作错误后的回滚
        db.session.rollback()
        #这个异常表示手机号出现重复值
        current_app.logger.error(e)
        return jsonify(errno=RET.DATAEXIST, errmsg="手机号已存在")
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(e)
        return jsonify(errno=RET.DATAEXIST, errmsg="查询数据库异常")
    # 保存登录状态到session中
    session["name"]=mobile
    session["mobile"] = mobile
    session["user_id"] = user.id
    #返回结果
    return jsonify(errno=RET.OK, errmsg="注册成功")

@api.route("/sessions",methods=['POST'])
def login():
    #参数：手机号、密码
    req_dict = request.get_json()
    # req_dict('mobile')拿到的是整个json串
    #req_dict = req_dict('mobile')
    print("req_dict",req_dict)
    mobile = req_dict['mobile']
    print("mobile:",mobile)
    password=req_dict['password']
    #参数完整性校验
    if not all([mobile,password]):
        return jsonify(errno=RET.PARAMERR,errmsg="参数不完整")
    #手机号格式
    if not re.match(r"1[35789]\d{9}",mobile):
        return jsonify(errno=RET.PARAMERR, errmsg="手机号格式不正确")
    #判断错误次数是否超过限制；如果超过，return
    #获取用户登录的ip--作为redis建值
    user_ip=request.remote_addr
    try:
        access_num=redis_store.get("access_num_%s"%user_ip)

    except Exception as e:
        current_app.logger.error(e)
    else:
        if access_num is not None and int(access_num)>=Const.LOGIN_ERROR_MAX_TIMES:
            return jsonify(errno=RET.REQERR, errmsg="错误次数过多，请稍候重试")
    #手机号和密码的匹配性
    try:
        user = User.query.filter_by(mobile=mobile).first()
        print("user-type:",type(user))
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="获取用户信息失败")
    if user is None or not user.check_password(password):
        #如果验证失败，记录错误次数，返回信息
        try:
            #将 key 中储存的数字值增一;如果 key 不存在，那么 key 的值会先被初始化为 0 ，然后再执行 INCR 操作
            redis_store.incr("access_num_%s"%user_ip)
            redis_store.expire("access_num_%s"%user_ip,Const.LOGIN_ERROR_FORBID_TIME)
        except Exception as e:
            current_app.logger.error(e)
        return jsonify(errno=RET.DATAERR, errmsg="用户名或密码错误")
    #如果验证成功，保存状态到session中
    session["name"]=user.name
    session["mobile"] = user.mobile
    session["user_id"] = user.id
    return jsonify(errno=RET.OK, errmsg="登录成功")
@api.route("/session",methods=["GET"])
def check_login():
    #检查登录状态
    name=session.get("name")
    if name is not None:
        return jsonify(errno=RET.OK, errmsg="true",data={"name":name})
    else:
        return jsonify(errno=RET.LOGINERR, errmsg="false")
@api.route("/session",methods=["DELETE"])
def logout():
    """登出"""
    session.clear()
    return jsonify(errno=RET.OK, errmsg="OK")