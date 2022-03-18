from common.BaseHandler import BaseHandler
from common.db.respondents import Respondents, query_respondents
from common.db.questionnaires import query_questionnaires
from common.db.delete import delete_respondents

from conf.base import (
    ERROR_CODE
)

from common.commons import http_response


class RegisterHandler(BaseHandler):
    def post(self):
        try:
            # 获取⼊参
            questionnaire_id = self.get_argument('questionnaireId')

            respondent = Respondents(questionnaireId=questionnaire_id)
            code = respondent.add()
            if code == '0':
                data = {
                    'respondentId': respondent.id
                }
                http_response(self, data, '0')
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
            # 修改完成问卷的人数
            questionnaire = query_questionnaires(respondent.questionnaireId, key='id')
            if complete != respondent.complete:
                if complete:
                    questionnaire.modify(questionnaire.respondentsCount + 1, key='respondentsCount')
                else:
                    questionnaire.modify(questionnaire.respondentsCount - 1, key='respondentsCount')
            if respondent:
                code = respondent.modify(complete, key='complete')
                http_response(self, ERROR_CODE[code], code)
        except Exception as e:
            # 获取⼊参失败时，抛出错误码及错误信息
            http_response(self, ERROR_CODE['1001'], '1001')
            print(f"ERROR： {e}")
