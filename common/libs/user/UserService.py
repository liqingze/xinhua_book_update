import hashlib, base64, random, string


class UserService():

    # cookie值中对uid加密
    @staticmethod
    def genAuthCode(user_info):
        m = hashlib.md5()
        str = "%s-%s-%s-%s" % (user_info.uid, user_info.login_name, user_info.login_pwd, user_info.login_salt)
        m.update(str.encode("utf-8"))
        return m.hexdigest()

    # 加密
    @staticmethod
    def genPwd(pwd, salt):
        m = hashlib.md5()
        str = "%s-%s" % (base64.encodebytes(pwd.encode("utf-8")), salt)
        m.update(str.encode("utf-8"))
        return m.hexdigest()

    # 生成随机加密码
    @staticmethod
    def genSalt(length=16):
        keylist = [random.choice((string.ascii_letters + string.digits)) for i in range(length)]
        return "".join(keylist)


if __name__ == '__main__':
    print(UserService.genPwd('123456', 'cF3JfH5FJfQ8B2Ba'))
