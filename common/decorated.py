from functools import wraps
import jwt
from common.db import (
    Respondents, query_respondents,
    RespondentsSummer, query_respondents_summer
)
from common.commons import http_response, token_encode, token_decode
from conf.base import ERROR_CODE


def respondent_login(method):
    @wraps(method)
    async def wrapper(self, *args, **kwargs):
        session_token = self.request.headers.get("Authorization-Resp", None)
        if session_token:
            # 对token过期进行异常捕捉
            try:
                # 从 token 中获得我们之前存进 payload 的用户id
                send_data = token_decode(session_token).get('data')
                respondent_id = send_data["id"]

                # 从数据库中获取到user并设置给_current_user
                try:
                    user: Respondents = query_respondents(respondent_id)
                    # 生成新的token，刷新保存时间

                    token = token_encode(user.id, 7)
                    res = {
                        'respondentId': user.id,
                        'token': token
                    }
                    http_response(self, res, '0')

                except Exception as e:
                    http_response(self, ERROR_CODE['2'], '2')
                    print(f"ERROR： {e}")

            except jwt.ExpiredSignatureError as e:
                http_response(self, ERROR_CODE['99'], '3')
                print(f"ERROR： {e}")
        else:
            # 此处需要使用协程方式执行 因为需要装饰的是一个协程
            method(self, *args, **kwargs)
    return wrapper


def respondent_auth(method):
    @wraps(method)
    async def wrapper(self, *args, **kwargs):
        session_token = self.request.headers.get("Authorization-Resp", None)
        if session_token:
            # 对token过期进行异常捕捉
            try:
                # 从 token 中获得我们之前存进 payload 的用户id
                send_data = token_decode(session_token).get('data')
                respondent_id = send_data["id"]

                # 从数据库中获取到user并设置给_current_user
                try:
                    respondent = query_respondents(respondent_id)
                    if respondent:
                        self.user = respondent
                        method(self, *args, **kwargs)
                    else:
                        http_response(self, ERROR_CODE['2'], '2')

                except Exception as e:
                    http_response(self, ERROR_CODE['2'], '2')
                    print(f"ERROR： {e}")

            except jwt.ExpiredSignatureError as e:
                http_response(self, ERROR_CODE['99'], '3')
                print(f"ERROR： {e}")
        else:
            http_response(self, ERROR_CODE['2'], '2')
    return wrapper


def summer_login(method):
    @wraps(method)
    async def wrapper(self, *args, **kwargs):
        session_token = self.request.headers.get("Authorization-Resp", None)
        if session_token:
            # 对token过期进行异常捕捉
            try:
                # 从 token 中获得我们之前存进 payload 的用户id
                send_data = token_decode(session_token).get('data')
                respondent_s_id = send_data["id"]

                # 从数据库中获取到user并设置给_current_user
                try:
                    user: RespondentsSummer = query_respondents(respondent_s_id)
                    # 生成新的token，刷新保存时间

                    token = token_encode(user.id, 7)
                    res = {
                        'id': user.id,
                        'token': token
                    }
                    http_response(self, res, '0')

                except Exception as e:
                    http_response(self, ERROR_CODE['2'], '2')
                    print(f"ERROR： {e}")

            except jwt.ExpiredSignatureError as e:
                http_response(self, ERROR_CODE['99'], '3')
                print(f"ERROR： {e}")
        else:
            # 此处需要使用协程方式执行 因为需要装饰的是一个协程
            method(self, *args, **kwargs)

    return wrapper


def respondent_s_auth(method):
    @wraps(method)
    async def wrapper(self, *args, **kwargs):
        session_token = self.request.headers.get("Authorization-Resp", None)
        if session_token:
            # 对token过期进行异常捕捉
            try:
                # 从 token 中获得我们之前存进 payload 的用户id
                send_data = token_decode(session_token).get('data')
                respondent_id = send_data["id"]

                # 从数据库中获取到user并设置给_current_user
                try:
                    respondent = query_respondents_summer(respondent_id)
                    if respondent:
                        self.user = respondent
                        method(self, *args, **kwargs)
                    else:
                        http_response(self, ERROR_CODE['2'], '2')

                except Exception as e:
                    http_response(self, ERROR_CODE['2'], '2')
                    print(f"ERROR： {e}")

            except jwt.ExpiredSignatureError as e:
                http_response(self, ERROR_CODE['99'], '3')
                print(f"ERROR： {e}")
        else:
            http_response(self, ERROR_CODE['2'], '2')
    return wrapper
