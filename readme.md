Python Flask 二手书平台
======================
### Linux:
* export ops_config=local|production && python manager.py runserver

* 使用flask-sqlacodegen扩展方便快速生成ORM model
pip install flask

###Windows:
* set ops_config=local|production && python manager.py runserver

* 使用flask-sqlacodegen扩展方便快速生成ORM model<br>
pip install flask-sqlacodegen<br>

    flask-sqlacodegen "mysql://数据库用户名:数据库密码@loc
alhost/数据库名称" --tables 表名 --outfile "生成路径" --f
lask

    ps:flask-sqlacodegen "mysql://root:root@loc
alhost/book_db" --tables user --outfile "common/models/User.py" --f
lask

* hasattr(object, name):对象中存在name返回True，否则False
* getattr(object, name):对象中存在name返回name值

* 小程序分享功能无法触发成功或失败的点击事件
百度（"微信小程序转发不执行success"）
2018年6月份新版微信客户端发布后，用户从App中分享小心给微信好友，或分享到朋友圈时，开发者将无法获知用户是否分享完成。具体调整点为：
（1）分享接口调用后，不再返回用户是否分享完成时间，即原先的cancel事件和success事件将统一为success事件

后期会删除微信分享统计功能，暂时做模拟数据展示

后台管理员: 账号：lee 密码：123456




