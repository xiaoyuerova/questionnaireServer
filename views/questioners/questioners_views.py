from common.BaseHandler import BaseHandler
from common.db.questioners import Questioners, query_questioners
from common.db.delete import delete_questioners

from conf.base import (
    ERROR_CODE
)

from common.commons import http_response


class RegisterHandler(BaseHandler):
    def post(self, *args, **kwargs):
        try:
            # 获取⼊参
            name = self.get_argument('name')
            email = self.get_argument('email')
            password = self.get_argument('password')

            questioner = Questioners(user_name=name, email=email, password=password)
            code = questioner.add()
            if code == '0':
                data = {
                    'questionerId': questioner.id
                }
                http_response(self, data, '0')
            else:
                http_response(self, ERROR_CODE[code], code)

        except Exception as e:
            # 获取⼊参失败时，抛出错误码及错误信息
            http_response(self, ERROR_CODE['1001'], '1001')
            print(f"ERROR： {e}")


class LoginHandler(BaseHandler):
    def post(self):
        try:
            # 获取⼊参
            name = self.get_argument('name')
            password = self.get_argument('password')

            ex_q = query_questioners(name)
            if ex_q:
                # 登录成功
                if ex_q.password == password:
                    data = {
                        'questionerId': ex_q.id
                    }
                    http_response(self, data, '0')
                else:
                    http_response(self, ERROR_CODE['1008'], '1008')
            else:
                http_response(self, ERROR_CODE['1007'], '1007')

        except Exception as e:
            # 获取⼊参失败时，抛出错误码及错误信息
            http_response(self, ERROR_CODE['1001'], '1001')
            print(f"ERROR： {e}")


class ELoginHandler(BaseHandler):
    def post(self):
        try:
            # 获取⼊参
            email = self.get_argument('email')
            password = self.get_argument('password')

            ex_q = query_questioners(email, key='email')
            if ex_q:
                # 登录成功
                if ex_q.password == password:
                    data = {
                        'questionerId': ex_q.id
                    }
                    http_response(self, data, '0')
                else:
                    http_response(self, ERROR_CODE['1008'], '1008')
            else:
                http_response(self, ERROR_CODE['1007'], '1007')

        except Exception as e:
            # 获取⼊参失败时，抛出错误码及错误信息
            http_response(self, ERROR_CODE['1001'], '1001')
            print(f"ERROR： {e}")


class DeleteHandler(BaseHandler):
    def post(self):
        try:
            # 获取⼊参
            ids = self.get_argument('questionerIds')

            if type(ids) == str:
                ids = eval(ids)
            code = delete_questioners(ids)
            if code == '0':
                http_response(self, ERROR_CODE['0'], '0')
            else:
                code, error_ids = code
                data = {
                    "errorIds": error_ids
                }
                http_response(self, data, code)
        except Exception as e:
            # 获取⼊参失败时，抛出错误码及错误信息
            http_response(self, ERROR_CODE['1001'], '1001')
            print(f"ERROR： {e}")
