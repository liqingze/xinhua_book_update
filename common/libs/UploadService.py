from werkzeug.utils import secure_filename
from application import app, db
from common.models.Image import Image
from common.libs.Helper import getCurrentDate
import os, stat, uuid


class UploadService():
    @staticmethod
    def uploadByFile(file):
        config_upload = app.config['UPLOAD']
        resp = {'code': 200, 'msg': '操作成功~~', 'data': {}}
        filename = secure_filename(file.filename)
        # 取上传文件的扩展名
        ext = filename.rsplit(".", 1)[0]

        if ext not in config_upload['ext']:
            resp['code'] = -1
            resp['msg'] = "不允许的扩张类型文件"
            return resp

        root_path = app.root_path + config_upload['prefix_path']
        file_dir = getCurrentDate("%Y%m%d")
        save_dir = root_path + '/' + file_dir
        if not os.path.exists(save_dir):
            os.mkdir(save_dir)
            # 权限
            os.chmod(save_dir, stat.S_IRWXU | stat.S_IRGRP | stat.S_IRWXO)

        # uuid根据硬件和时间统一生成一个唯一的不重复的字符串
        file_name = str(uuid.uuid4()).replace("-", "") + "." + ext
        file.save("{0}/{1}".format(save_dir, file_name))

        # 图片存入数据库
        model_image = Image()
        model_image.file_key = file_dir + "/" + file_name
        model_image.created_time = getCurrentDate()
        db.session.add(model_image)
        db.session.commit()

        resp['data'] = {
            'file_key': model_image.file_key
        }

        return resp
