import json, requests, datetime
from application import app, db
from common.models.queue.QueueList import QueueList
from common.libs.Helper import getCurrentDate
from common.models.pay.PayOrder import PayOrder
from common.models.pay.PayOrderItem import PayOrderItem
from common.models.book.Book import Book
from common.libs.pay.WeChatService import WeChatService
from common.models.member.OauthMemberBind import OauthMemberBind
from common.models.book.BookSaleChangeLog import BookSaleChangeLog
from sqlalchemy import func

"""
python manager.py runjob -m queue/index
"""


class JobTask():
    def __init__(self):
        pass

    def run(self, params):
        list = QueueList.query.filter_by(status=-1).order_by(QueueList.id.asc()).limit(1).all()
        for item in list:
            if item.queue_name == "pay":
                self.handlePay(item)

            item.status = 1
            item.updated_time = getCurrentDate()
            db.session.add(item)
            db.session.commit()

    def handlePay(self, item):
        data = json.loads(item)
        if 'member_id' not in data or 'pay_order_id' not in data:
            return False

        oauth_bind_info = OauthMemberBind.query.filter_by(member_id=data['member_id']).first()
        if not oauth_bind_info:
            return False

        pay_order_info = PayOrder.query.filter_by(id=data['pay_order_id']).first()
        if not pay_order_info:
            return False

        pay_order_items = PayOrderItem.query.filter_by(pay_order_id=pay_order_info.id).all()
        notice_content = []
        # 更新销售数量
        if pay_order_items:
            date_from = datetime.datetime.now().strftime("%Y-%m-01 00:00:00")
            date_to = datetime.datetime.now().strftime("%Y-%m-31 23:59:59")
            for item in pay_order_items:
                tmp_book_info = Book.query.filter_by(id=item.book_id).first()
                if not tmp_book_info:
                    continue

                notice_content.append("《%s》 %s份" % (tmp_book_info.name, item.quantity))

                # 当月的销量
                tmp_stat_info = db.session.query(BookSaleChangeLog, func.sum(BookSaleChangeLog.quantity).label('total'))\
                    .filter(BookSaleChangeLog.book_id == item.book_id)\
                    .filter(BookSaleChangeLog.created_time >= date_from, BookSaleChangeLog.created_time <= date_to).first()
                tmp_month_count = tmp_stat_info[1] if tmp_stat_info[1] else 0
                tmp_book_info.total_count += 1
                tmp_book_info.month_count = 0
                db.session.add(tmp_book_info)
                db.session.commit()

        keyword1_val = "、".join(notice_content)
        keyword2_val = str(pay_order_info.total_price)
        keyword3_val = str(pay_order_info.order_number)
        keyword4_val = ""  # todo

        target_wechat = WeChatService()
        access_token = target_wechat.getAccessToken()

        headers = {'Content-Type': 'application/xml'}
        url = "https://api.weixin.qq.com/cgi-bin/message/wxopen/template/send?access_token=%s" % access_token

        params = {
            "touser": oauth_bind_info.openid,
            "template_id": "j4XkDmbp6uXuho20Z63xBElSW9gupExdq44cbKGUoIc",
            "page": "pages/my/order_list",
            "form_id": pay_order_info.prepay_id,
            "data": {
                "keyword1": {
                    "value": keyword1_val
                },
                "keyword2": {
                    "value": keyword2_val
                },
                "keyword3": {
                    "value": keyword3_val
                },
                "keyword4": {
                    "value": keyword4_val
                }
            }
        }

        r = requests.post(url=url, data=json.dumps(params), headers=headers)
        r.encoding = "utf-8"
        app.logger.info(r.text)
        return True
