from common.BaseHandler import BaseHandler
from common.db.answers import Answers

from conf.base import (
    ERROR_CODE
)

from common.commons import http_response
from common.db.respondents import query_respondents


class SubmitHandler(BaseHandler):
    def post(self):
        try:
            # 获取⼊参
            respondent_id = self.get_argument('respondentId')
            questionnaire_id = self.get_argument('questionnaireId')
            reference = self.get_argument('reference')
            answers = self.get_argument('answers')

            respondent = query_respondents(respondent_id, key='respondentId')
            if not respondent:
                http_response(self, ERROR_CODE['5002'], '5002')
            # question = Questions(questionnaireId=questionnaire_id, type=_type, question=question, options=options,
            #                      options_count=options_count)
            # code = question.add()
            http_response(self, ERROR_CODE['0'], '0')

        except Exception as e:
            # 获取⼊参失败时，抛出错误码及错误信息
            http_response(self, ERROR_CODE['3001'], '3001')
            print(f"ERROR： {e}")
