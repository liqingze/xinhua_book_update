from web.contorllers.api import route_api
from flask import request, jsonify, g
from application import app, db
import requests, json
from common.libs.Helper import getCurrentDate, getDictFilterField, selectFilterObj
from common.libs.UrlManager import UrlManager
from common.models.book.BookCat import BookCat
from common.models.book.Book import Book
from common.models.member.MemberCart import MemberCart
from common.models.book.BookStockChangeLog import BookStockChangeLog
from common.models.member.MemberComments import MemberComments
from common.models.member.Member import Member
from sqlalchemy import or_
from decimal import Decimal


@route_api.route("/book/index")
def bookIndex():
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    cat_list = BookCat.query.filter_by(status=1).order_by(BookCat.weight.desc()).all()
    data_cat_list = [
        {
            'id': 0,
            'name': '全部',
        }
    ]
    if cat_list:
        for item in cat_list:
            tmp_data = {
                "id": item.id,
                "name": item.name
            }
            data_cat_list.append(tmp_data)
    resp['data']['cat_list'] = data_cat_list

    book_list = Book.query.filter_by(status=1) \
        .order_by(Book.total_count.desc(), Book.id.desc()).limit(3).all()
    data_book_list = []
    if book_list:
        for item in book_list:
            tmp_data = {
                "id": item.id,
                "pic_url": UrlManager.buildImageUrl(item.main_image)
            }
            data_book_list.append(tmp_data)
    resp['data']['banner_list'] = data_book_list
    return jsonify(resp)


@route_api.route("/book/search")
def bookSearch():
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    req = request.values
    cat_id = int(req['cat_id']) if 'cat_id' in req else 0
    mix_kw = str(req['mix_kw']) if 'mix_kw' in req else ''
    p = int(req['p']) if 'p' in req else 1
    if p < 1:
        p = 1

    query = Book.query.filter_by(status=1)

    page_size = 10
    offset = (p - 1) * page_size

    if cat_id > 0:
        query = query.filter(Book.cat_id == cat_id)

    if mix_kw:
        rule = or_(Book.name.ilike("%{0}%".format(mix_kw)), Book.tags.ilike("%{0}%".format(mix_kw)))
        query = query.filter(rule)

    book_list = query.order_by(Book.total_count.desc(), Book.id.desc()) \
        .offset(offset).limit(page_size).all()
    data_book_list = []
    if book_list:
        for item in book_list:
            tmp_data = {
                'id': item.id,
                'name': item.name,
                'price': str(item.price),
                'min_price': str(item.price),
                'pic_url': UrlManager.buildImageUrl(item.main_image)
            }
            data_book_list.append(tmp_data)

    resp['data']['list'] = data_book_list
    resp['data']['has_more'] = 0 if len(data_book_list) < page_size else 1

    return jsonify(resp)


@route_api.route("/book/info")
def bookInfo():
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    req = request.values
    id = int(req['id']) if 'id' in req else 0
    book_info = Book.query.filter_by(id=id).first()
    if not book_info or not book_info.status:
        resp['code'] = -1
        resp['msg'] = '书籍已下架~~',
        return jsonify(resp)

    member_info = g.member_info
    cart_number = 0
    if member_info:
        cart_number = MemberCart.query.filter_by(member_id=member_info.id).count()

    resp['data']['info'] = {
        "id": book_info.id,
        "name": book_info.name,
        "summary": book_info.summary,
        "total_count": book_info.total_count,
        "comment_count": book_info.comment_count,
        "main_image": UrlManager.buildImageUrl(book_info.main_image),
        "price": str(book_info.price),
        "stock": book_info.stock,
        "pics": [UrlManager.buildImageUrl(book_info.main_image)]
    }
    resp['data']['cart_number'] = cart_number
    return jsonify(resp)


@route_api.route("/book/comments")
def bookComments():
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    req = request.values
    id = int(req['id']) if 'id' in req else 0
    query = MemberComments.query.filter(MemberComments.book_ids.ilike("%_{0}_%".format(id)))
    list = query.order_by(MemberComments.id.desc()).limit(5).all()
    data_list = []
    if list:
        member_map = getDictFilterField(Member, Member.id, "id", selectFilterObj(list, "member_id"))
        for item in list:
            if item.member_id not in member_map:
                continue
            tmp_member_info = member_map[item.member_id]
            tmp_data = {
                'score': item.score_desc,
                'date': item.created_time.strftime("%Y-%m-%d %H:%M:%S"),
                "content": item.content,
                "user": {
                    'nickname': tmp_member_info.nickname,
                    'avatar_url': tmp_member_info.avatar,
                }
            }
            data_list.append(tmp_data)
    resp['data']['list'] = data_list
    resp['data']['count'] = query.count()
    return jsonify(resp)
