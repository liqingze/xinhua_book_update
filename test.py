# context = {}
# g = {'name': 'lee', 'age': 18}
# if 'aaaa' in g:
#     context['name'] = g['name']
#     print(context)
# else:
#     print('1')
# resp_data = {}
# list = [1, 2, 3, 4]
# resp_data['list'] = list
# print(resp_data)
import random, string
from common.models.User import User
from sqlalchemy import or_
import re
from common.libs.Helper import selectFilterObj

# keylist = [random.choice((string.ascii_letters + string.digits)) for i in range(16)]
# print("".join(keylist))
# STATUS_MAPPING = {
#     "1": "正常",
#     "0": "已删除"
# }
# for i in STATUS_MAPPING:
#     print(type(i), STATUS_MAPPING[i])
#
# print(STATUS_MAPPING[str(1)])
# rule = "%{0}%".format("何勇霖")
# print(rule)
# resp = {'data': {}}
# resp['data']['list'] = 'name'
# print(resp)
import datetime

# old = datetime.datetime.now()
# date = old + datetime.timedelta(seconds=7200)
# now = date.strftime("%Y-%m-%d %H:%M:%S")
# print(now)
# print(date)
# pay_order_items_map = {'1': [1, 2], '2': [2, 3]}
# book_ids = []
# for item in pay_order_items_map:
#     tmp_book_ids = selectFilterObj(pay_order_items_map[item], "book_id")
#     tmp_book_ids = {}.fromkeys(tmp_book_ids).keys()
#     book_ids = book_ids + list(tmp_book_ids)
#     print(tmp_book_ids)
# print(book_ids)
id = 1
print("%_{0}_%".format(id))
