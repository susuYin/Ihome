import json
import re

from flask import request, jsonify, current_app, session
from sqlalchemy.exc import IntegrityError
from ihome import redis_store, db, Const
from ihome.models import User
from ihome.utils.response_code import RET
from ihome.models import Area
from . import api
@api.route("/areas")
def get_area_info():
    #从redis信息
    try:
        resp_json=redis_store.get("area_info")
    except Exception as e:
        current_app.logger.error(e)
    else:
        if resp_json is not None:
            current_app.logger.info("从redis中读取成功")
            return resp_json,200,{"Content-Type": "application/json"}
    #从数据库查询城区信息
    all_area_list=[]
    try:
        all_area=Area.query.all()
    except Exception as  e:
        current_app.logger.error(e)
        return  jsonify(errno=RET.DBERR,errmsg="数据库查询异常")
    for area in all_area:
        #将对象转换为字典
        all_area_list.append(area.to_dict())
    #将数据转换为json
    resp_dict=dict(errno=RET.OK,errmsg="OK",data=all_area_list)
    resp_json=json.dumps(resp_dict)
    #将数据保存到redis当中
    try:
        redis_store.setex("area_info",Const.AREA_INFO_REDIS_CACHE_EXPIRES,resp_json)
    except Exception as  e:
        current_app.logger.error(e)
        return  jsonify(errno=RET.DBERR,errmsg="城区信息缓存失败")
    return resp_json,200,{"Content-Type":"application/json"}
