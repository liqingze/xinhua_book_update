from flask import Blueprint

route_api = Blueprint('api_page', __name__)
from web.contorllers.api.Member import *
from web.contorllers.api.Book import *
from web.contorllers.api.Cart import *
from web.contorllers.api.Order import *
from web.contorllers.api.My import *
from web.contorllers.api.Address import *


@route_api.route("/")
def index():
    return "Mina Api V1.0~~"
