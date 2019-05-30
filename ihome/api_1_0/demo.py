
from . import api

@api.route("/index")
def index():
    # session[]=""
    # session.get()
    return "index page"