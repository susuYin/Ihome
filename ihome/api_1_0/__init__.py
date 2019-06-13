from flask import Blueprint
##创建蓝图对象
#Blueprint必须指定两个参数，admin表示蓝图的名称，__name__表示蓝图所在模块
api=Blueprint("api_1_0",__name__)
##导入蓝图的视图
from . import demo,verifyCode,passport

