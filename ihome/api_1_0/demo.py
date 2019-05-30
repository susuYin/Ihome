
from . import api
import logging
from flask import current_app
from  ihome import db,models

@api.route("/index")
def index():

    logging.debug("进入首页了")
    current_app.logger.error("出错了")
    # session[]=""
    # session.get()

    return "index page"