from common.BaseHandler import BaseHandler
from common.db import (
    Respondents,
    query_respondents,
    query_questionnaires,
    query_questions,
    query_answers,
    delete_respondents
)
from views.respondents.utils import complete_handler
from common.commons import token_encode
from common.decorated import respondent_login, respondent_auth

from conf.base import (
    ERROR_CODE
)

from common.commons import http_response


class RegisterHandler(BaseHandler):
    @respondent_login
    def post(self):
        try:
            # 获取⼊参
            questionnaire_id = self.get_argument('questionnaireId')

            respondent = Respondents(questionnaireId=questionnaire_id)
            code = respondent.add()
            if code == '0':
                token = token_encode(respondent.id, 7)
                print(token)
                res = {
                    'respondentId': respondent.id,
                    'token': token
                }
                http_response(self, res, '0')
            else:
                http_response(self, ERROR_CODE[code], code)

        except Exception as e:
            # 获取⼊参失败时，抛出错误码及错误信息
            http_response(self, ERROR_CODE['3001'], '3001')
            print(f"ERROR： {e}")


class DeleteHandler(BaseHandler):
    def post(self):
        try:
            # 获取⼊参
            ids = self.get_argument('respondentIds')

            if type(ids) == str:
                ids = eval(ids)
            code = delete_respondents(ids)
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


class CompleteHandler(BaseHandler):
    @respondent_auth
    def post(self):
        try:
            # 获取⼊参
            id_ = self.get_argument('respondentId')
            complete = self.get_argument('complete')

            if type(id_) == str:
                id_ = eval(id_)
            if type(complete) == str:
                complete = eval(complete)
            respondent = query_respondents(id_, key='id')
            questionnaire = query_questionnaires(respondent.questionnaireId, key='id')
            # 判断作答是否全部完成
            questions = query_questions(questionnaire.id, key='questionnaireId', search_all=True)
            answers = query_answers(respondent.id, key='respondentId', search_all=True)
            if not questions:
                # 问卷没有题目，肯定出问题了
                http_response(self, ERROR_CODE['4004'], '4004')
                return
            if not answers:
                http_response(self, ERROR_CODE['4004'], '4004')
                return
            if not len(questions) == len(answers):
                http_response(self, ERROR_CODE['4004'], '4004')
                return
            # 修改完成问卷的人数
            if complete != respondent.complete:
                if complete:
                    complete_handler(answers)
                else:
                    complete_handler(answers, de_complete=True)
            code = respondent.modify(complete, key='complete')
            http_response(self, ERROR_CODE[code], code)
        except Exception as e:
            # 获取⼊参失败时，抛出错误码及错误信息
            http_response(self, ERROR_CODE['1001'], '1001')
            print(f"ERROR： {e}")
