from flask import session, g, jsonify
from werkzeug.routing import BaseConverter
###定义一个正则转换器
from ihome.utils.response_code import RET
import functools

class ReConverter(BaseConverter):
    def __init__(self,url_map,regex):
        ##调用父类初始化方法
        super(ReConverter,self).__init__(url_map)
        #保存正则表达式
        self.regex=regex
###定义验证登录状态的装饰器
def login_required(view_func):
    # wraps函数的作用是将wrapper内层函数的属性设置为被装饰函数view_func的属性
    #增加@functools.wraps(f), 可以保持当前装饰器去装饰的函数的属性值不变
    @functools.wraps(view_func)
    def wrapper(*args,**kwargs):
        ##判断用户登录状态
        user_id=session.get("user_id")
        #如果登录，执行视图函数
        if user_id is not None:
            g.user_id=user_id
            return view_func(*args,**kwargs)
        #如果未登录，返回未登录信息
        else:
            return jsonify(errno=RET.SESSIONERR, errmsg="用户未登录")
    return wrapper



