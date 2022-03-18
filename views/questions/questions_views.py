from common.BaseHandler import BaseHandler
from common.db.questions import Questions
from common.db.delete import delete_questions

from conf.base import (
    ERROR_CODE
)

from common.commons import http_response


class CreateHandler(BaseHandler):
    def post(self):
        try:
            # 获取⼊参
            questionnaire_id = self.get_argument('questionnaireId')
            question_number = self.get_argument('questionNumber')
            _type = self.get_argument('type')
            question = self.get_argument('question')
            options = self.get_argument('options')
            options_count = self.get_argument('options_count')

            question = Questions(questionnaireId=questionnaire_id, questionNumber=question_number, type=_type,
                                 question=question, options=options, optionsCount=options_count)
            code = question.add()
            http_response(self, ERROR_CODE[code], code)

        except Exception as e:
            # 获取⼊参失败时，抛出错误码及错误信息
            http_response(self, ERROR_CODE['3001'], '3001')
            print(f"ERROR： {e}")


class DeleteHandler(BaseHandler):
    def post(self):
        try:
            # 获取⼊参
            ids = self.get_argument('questionIds')

            if type(ids) == str:
                ids = eval(ids)
            code = delete_questions(ids)
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
