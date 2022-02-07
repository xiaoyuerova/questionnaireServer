from common.BaseHandler import BaseHandler
from common.db.questioners import Questioners, query_questioners

from conf.base import (
    ERROR_CODE
)

from common.commons import http_response


class RegisterHandler(BaseHandler):
    def post(self, *args, **kwargs):
        try:
            # 获取⼊参
            name = self.get_argument('name')
            password = self.get_argument('password')

            questioner = Questioners(user_name=name, password=password)
            code = questioner.add()
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
                if ex_q.password == password:
                    http_response(self, ERROR_CODE['0'], '0')
                else:
                    http_response(self, ERROR_CODE['1008'], '1008')
            else:
                http_response(self, ERROR_CODE['1007'], '1007')

        except Exception as e:
            # 获取⼊参失败时，抛出错误码及错误信息
            http_response(self, ERROR_CODE['1001'], '1001')
            print(f"ERROR： {e}")
