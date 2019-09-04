from application import app

'''
统计拦截器
'''
from web.interceptors.AuthInterceptor import *
from web.interceptors.ApiAuthInterceptor import *
from web.interceptors.ErrorInterceptor import *

'''
蓝图功能，对所有的url进行蓝图功能配置
'''

from web.contorllers.index import route_index
from web.contorllers.User.User import route_user
from web.contorllers.Account.Account import route_account
from web.contorllers.Finance.Finance import route_finance
from web.contorllers.Book.Book import route_book
from web.contorllers.Stat.Stat import route_stat
from web.contorllers.Member.Member import route_member
from web.contorllers.api import route_api
from web.contorllers.upload.Upload import route_upload
from web.contorllers.chart import route_chart

app.register_blueprint(route_index, url_prefix="/")
app.register_blueprint(route_user, url_prefix="/user")
app.register_blueprint(route_account, url_prefix="/account")
app.register_blueprint(route_finance, url_prefix="/finance")
app.register_blueprint(route_book, url_prefix="/book")
app.register_blueprint(route_stat, url_prefix="/stat")
app.register_blueprint(route_member, url_prefix="/member")
app.register_blueprint(route_api, url_prefix="/api")
app.register_blueprint(route_upload, url_prefix="/upload")
app.register_blueprint(route_chart, url_prefix="/chart")
