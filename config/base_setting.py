SERVER_PORT = 8080
DEBUG = False
SQLALCHEMY_ECHO = False
SQLALCHEMY_DATABASE_URI = "mysql://root:root@127.0.0.1/book_db?charset=utf8mb4"
SQLALCHEMY_TRACK_MODIFICATIONS = False
AUTH_COOKIE_NAME = "xinhua_book"


SEO_TITLE = "Python Flask小程序"

##过滤url
IGNORE_URLS = [
    "^/user/login",
]

IGNORE_CHECK_LOGIN_URLS = [
    "^/static",
    "^/favicon.ico"
]

##过滤会员url
API_IGNORE_URLS = [
    "^/api"
]

PAGE_SIZE = 50
PAGE_DISPLAY = 10

STATUS_MAPPING = {
    "1": "正常",
    "0": "已删除"
}
MINA_APP = {
    'appid': 'wx1f79d8a5ac7c2c0d',
    'appkey': 'c237cc39be472d1c5317436463a35685',
    'paykey': '',
    'mch_id': '',
    'callback_url': 'api/order/callback'
}

UPLOAD = {
    'ext': ['jpg', 'gif', 'bmp', 'jpeg', 'png'],
    'prefix_path': '/static/upload/',
    'prefix_url': '/static/upload/'
}

APP = {
    'domain': 'http://localhost:8080'
}

PAY_STATUS_MAPPING = {
    "1": "已支付",
    "-8": "待支付",
    "0": "已关闭"
}

PAY_STATUS_DISPLAY_MAPPING = {
    "0": "订单关闭",
    "1": "支付成功",
    "-8": "待支付",
    "-7": "待发货",
    "-6": "待确认",
    "-5": "待评价",
}
