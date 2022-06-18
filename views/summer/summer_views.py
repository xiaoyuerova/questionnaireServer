from common.BaseHandler import BaseHandler
from common.commons import token_encode, http_response
from common.db import *
from common.decorated import summer_login
from conf.base import ERROR_CODE


class LoginHandler(BaseHandler):
    @summer_login
    def post(self):
        try:
            # 获取⼊参
            user_name = self.get_argument('userName')
            password = self.get_argument('password')

            respondent_s: RespondentsSummer = query_respondents_summer(user_name, key='userName')

            if password == respondent_s.password:
                token = token_encode(respondent_s.id, 7)
                print(token)
                res = {
                    'id': respondent_s.id,
                    'token': token
                }
                http_response(self, res, '0')
            else:
                http_response(self, ERROR_CODE['6006'], '6006')

        except Exception as e:
            # 获取⼊参失败时，抛出错误码及错误信息
            http_response(self, ERROR_CODE['6001'], '6001')
            print(f"ERROR： {e}")
