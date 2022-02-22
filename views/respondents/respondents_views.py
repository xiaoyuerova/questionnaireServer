from common.BaseHandler import BaseHandler
from common.db.respondents import Respondents
from common.db.questionnaires import query_questionnaires

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
                questionnaire = query_questionnaires(questionnaire_id, key='id')
                questionnaire.modify(questionnaire.respondentsCount + 1, key='respondentsCount')
            else:
                http_response(self, ERROR_CODE[code], code)

        except Exception as e:
            # 获取⼊参失败时，抛出错误码及错误信息
            http_response(self, ERROR_CODE['3001'], '3001')
            print(f"ERROR： {e}")
