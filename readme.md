Python Flask 二手书平台
======================
### Linux:
* export ops_config=local|production && python manager.py runserver

### Windows:
* set ops_config=local|production && python manager.py runserver

* 小程序分享功能无法触发成功或失败的点击事件
百度（"微信小程序转发不执行success"）
2018年6月份新版微信客户端发布后，用户从App中分享小心给微信好友，或分享到朋友圈时，开发者将无法获知用户是否分享完成。具体调整点为：
（1）分享接口调用后，不再返回用户是否分享完成时间，即原先的cancel事件和success事件将统一为success事件

后期会删除微信分享统计功能，暂时做模拟数据展示

微信支付，获取会员手机号码和评价等功能还待完善
