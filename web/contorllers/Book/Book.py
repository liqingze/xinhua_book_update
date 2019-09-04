from flask import Blueprint, request, jsonify, redirect
from common.libs.UrlManager import UrlManager
from common.libs.Helper import ops_render, getCurrentDate, getDictFilterField
from common.models.book.BookCat import BookCat
from common.models.book.Book import Book
from common.libs.Helper import iPagination
from common.models.book.BookStockChangeLog import BookStockChangeLog
from common.libs.book.BookService import BookService
from application import app, db
from decimal import Decimal
from sqlalchemy import or_

route_book = Blueprint('book_page', __name__)


@route_book.route("/index")
def index():
    resp_data = {}
    req = request.values
    page = int(req['p']) if ('p' in req and req['p']) else 1
    query = Book.query
    if 'mix_kw' in req:
        rule = or_(Book.name.ilike("%{0}%".format(req['mix_kw'])), Book.tags.ilike("%{0}%".format(req['mix_kw'])))
        query = query.filter(rule)

    if 'status' in req and int(req['status']) > -1:
        query = query.filter(Book.status == int(req['status']))

    if 'cat_id' in req and int(req['cat_id']) > -1:
        query = query.filter(Book.cat_id == int(req['cat_id']))

    page_params = {
        'total': query.count(),
        'page_size': app.config['PAGE_SIZE'],
        'page': page,
        'display': app.config['PAGE_DISPLAY'],
        'url': request.full_path.replace("&p={}".format(page), "")
    }

    pages = iPagination(page_params)
    offset = (page - 1) * app.config['PAGE_SIZE']

    list = query.order_by(Book.id.desc()).offset(offset).limit(app.config['PAGE_SIZE']).all()

    cat_mapping = getDictFilterField(BookCat, BookCat.id, "id", [])
    resp_data['list'] = list
    resp_data['pages'] = pages
    resp_data['search_con'] = req
    resp_data['cat_mapping'] = cat_mapping
    resp_data['status_mapping'] = app.config['STATUS_MAPPING']
    resp_data['current'] = 'index'
    return ops_render("book/index.html", resp_data)


@route_book.route("/info")
def info():
    resp_data = {}
    req = request.args
    id = int(req.get("id", 0))
    reback_url = UrlManager.buildUrl("/book/index")

    if id < 1:
        return redirect(reback_url)

    info = Book.query.filter_by(id=id).first()
    if not info:
        return redirect(reback_url)

    stock_change_list = BookStockChangeLog.query.filter(BookStockChangeLog.book_id == id)\
        .order_by(BookStockChangeLog.id.desc()).all()

    resp_data['info'] = info
    resp_data['stock_change_list'] = stock_change_list
    resp_data['current'] = 'index'
    return ops_render("book/info.html", resp_data)


@route_book.route("/set", methods=["GET", "POST"])
def set():
    if request.method == "GET":
        resp_data = {}
        req = request.args
        id = int(req.get('id', 0))
        print(id)
        info = Book.query.filter_by(id=id).first()
        if info and info.status != 1:
            return redirect(UrlManager.buildUrl('/book/index'))
        cat_list = BookCat.query.all()
        resp_data['info'] = info
        resp_data['cat_list'] = cat_list
        resp_data['current'] = 'set'
        print(info)
        return ops_render("book/set.html", resp_data)

    resp = {'code': 200, 'msg': '操作成功~~', 'data': {}}
    req = request.values
    id = int(req['id']) if 'id' in req and req['id'] else 0
    cat_id = int(req['cat_id']) if 'cat_id' in req else 0
    name = req['name'] if 'name' in req else ''
    price = req['price'] if 'price' in req else ''
    main_image = req['main_image'] if 'main_image' in req else ''
    summary = req['summary'] if 'summary' in req else ''
    stock = int(req['stock']) if 'stock' in req else ''
    tags = req['tags'] if 'tags' in req else ''

    if cat_id < 1:
        resp['code'] = -1
        resp['msg'] = "请选择分类~~"
        return jsonify(resp)

    if name is None or len(name) < 1:
        resp['code'] = -1
        resp['msg'] = "请输入符合规范的名称~~"
        return jsonify(resp)

    if not price or len(price) < 1:
        resp['code'] = -1
        resp['msg'] = "请输入符合规范的售卖价格~~"
        return jsonify(resp)

    price = Decimal(price).quantize(Decimal('0.00'))
    if price <= 0:
        resp['code'] = -1
        resp['msg'] = "请输入符合规范的售卖价格~~"
        return jsonify(resp)

    if main_image is None or len(main_image) < 3:
        resp['code'] = -1
        resp['msg'] = "请上传封面图~~"
        return jsonify(resp)

    if summary is None or len(summary) < 3:
        resp['code'] = -1
        resp['msg'] = "请输入图书描述，并不能少于10个字符~~"
        return jsonify(resp)

    if stock < 1:
        resp['code'] = -1
        resp['msg'] = "请输入符合规范的库存量~~"
        return jsonify(resp)

    if tags is None or len(tags) < 1:
        resp['code'] = -1
        resp['msg'] = "请输入标签，便于搜索~~"
        return jsonify(resp)

    book_info = Book.query.filter_by(id=id).first()
    before_stock = 0
    if book_info:
        model_book = book_info
        before_stock = model_book.stock
    else:
        model_book = Book()
        model_book.status = 1
        model_book.created_time = getCurrentDate()

    model_book.cat_id = cat_id
    model_book.name = name
    model_book.price = price
    model_book.main_image = main_image
    model_book.summary = summary
    model_book.stock = stock
    model_book.tags = tags
    model_book.updated_time = getCurrentDate()

    db.session.add(model_book)
    db.session.commit()

    BookService.setStockChangeLog(model_book.id, int(stock) - int(before_stock), "后台修改")

    return jsonify(resp)


@route_book.route("/cat")
def cat():
    resp_data = {}
    req = request.values
    query = BookCat.query

    if 'status' in req and int(req['status']) > -1:
        query = query.filter(BookCat.status == int(req['status']))

    list = query.order_by(BookCat.weight.desc(), BookCat.id.desc()).all()
    resp_data['list'] = list
    resp_data['search_con'] = req
    resp_data['status_mapping'] = app.config['STATUS_MAPPING']
    resp_data['current'] = 'cat'

    return ops_render("book/cat.html", resp_data)


@route_book.route("/cat_set", methods=["GET", "POST"])
def cat_set():
    if request.method == "GET":
        resp_data = {}
        req = request.args
        id = int(req.get("id", 0))
        info = None
        if id:
            info = BookCat.query.filter_by(id=id).first()
        resp_data['info'] = info
        resp_data['current'] = 'cat_set'
        return ops_render("book/cat_set.html", resp_data)

    resp = {'code': 200, 'msg': '操作成功~~', 'data': {}}
    req = request.values

    id = req['id'] if 'id' in req else 0
    name = req['name'] if 'name' in req else ''
    weight = int(req['weight']) if ('weight' in req and int(req['weight']) > 0) else 1

    if name is None or len(name) < 1:
        resp['code'] = -1
        resp['msg'] = "请输入符合规范的分类名称~~"
        return jsonify(resp)

    book_cat_info = BookCat.query.filter_by(id=id).first()
    if book_cat_info:
        model_book_cat = book_cat_info

    else:
        model_book_cat = BookCat()
        model_book_cat.created_time = getCurrentDate()
    model_book_cat.name = name
    model_book_cat.weight = weight
    model_book_cat.updated_time = getCurrentDate()

    db.session.add(model_book_cat)
    db.session.commit()
    return jsonify(resp)


# 删除和恢复功能
@route_book.route("/cat-ops", methods=["POST"])
def cat_ops():
    resp = {'code': 200, 'msg': '操作成功~~', 'data': {}}
    req = request.values

    id = req['id'] if 'id' in req else 0
    act = req['act'] if 'act' in req else ''
    if not id:
        resp['code'] = -1
        resp['msg'] = "请选择要操作的账号~~"
        return jsonify(resp)

    if act not in ['remove', 'recover']:
        resp['code'] = -1
        resp['msg'] = "操作有误，请重试~~"
        return jsonify(resp)

    book_cat_info = BookCat.query.filter_by(id=id).first()
    if not book_cat_info:
        resp['code'] = -1
        resp['msg'] = "指定账号不存在~~"
        return jsonify(resp)
    if act == "remove":
        book_cat_info.status = 0
    elif act == "recover":
        book_cat_info.status = 1

    book_cat_info.updated_time = getCurrentDate()
    db.session.add(book_cat_info)
    db.session.commit()
    return jsonify(resp)


@route_book.route("/ops", methods=["POST"])
def ops():
    resp = {'code': 200, 'msg': '操作成功~~', 'data': {}}
    req = request.values
    id = req['id'] if 'id' in req else 0
    act = req['act'] if 'act' in req else ''

    if not id:
        resp['code'] = -1
        resp['msg'] = "请选择要操作的账号~~"
        return jsonify(resp)

    if act not in ['remove', 'recover']:
        resp['code'] = -1
        resp['msg'] = "操作有误，请重试~~"
        return jsonify(resp)

    book_info = Book.query.filter_by(id=id).first()
    if not book_info:
        resp['code'] = -1
        resp['msg'] = "指定书籍不存在~~"
        return jsonify(resp)

    if act == "remove":
        book_info.status = 0
    elif act == "recover":
        book_info.status = 1

    book_info.updated_time = getCurrentDate()
    db.session.add(book_info)
    db.session.commit()
    return jsonify(resp)

