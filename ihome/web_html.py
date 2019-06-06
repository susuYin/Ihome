from flask import Blueprint, current_app, make_response
from flask_wtf import csrf
##提供静态文件的蓝图
html=Blueprint("web.html",__name__)
@html.route("/<re(r'.*'):file_name>")
def  get_html(file_name):
    """提供html文件"""
    if not file_name:
        file_name="index.html"
    ##如果资源名不是favicon.ico时，才拼接路径
    if file_name!="favicon.ico":
        file_name="html/"+file_name
    ###创建csrf_token值
    csrf_token=csrf.generate_csrf()
    resp=make_response(current_app.send_static_file(file_name))
    #return  make_response(current_app.send_static_file(file_name))
    ##设置cookie值
    resp.set_cookie("csrf_token",csrf_token)
    return  resp

