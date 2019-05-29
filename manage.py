from flask import Flask,session
from flask_sqlalchemy import SQLAlchemy
import redis
from flask_session import Session
from flask_wtf import CSRFProtect
from config import config_map
#####目的：开启flask框架
from ihome import creat_app

app=creat_app("dev")





@app.route("/index")
def index():
    # session[]=""
    # session.get()
    return "index page"

if __name__ == '__main__':
    app.run()