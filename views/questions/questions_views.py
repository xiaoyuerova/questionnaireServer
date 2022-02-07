from common.BaseHandler import BaseHandler
from common.db.questions import Questions, query_questions

from conf.base import (
    ERROR_CODE
)

from common.commons import http_response


class CreateHandler(BaseHandler):
    def post(self):
        try:
            # 获取⼊参
            questionnaire_id = self.get_argument('questionnaireId')
            _type = self.get_argument('type')
            question = self.get_argument('question')
            options = self.get_argument('options')
            options_count = self.get_argument('options_count')

            question = Questions(questionnaireId=questionnaire_id, type=_type, question=question, options=options,
                                 options_count=options_count)
            code = question.add()
            http_response(self, ERROR_CODE[code], code)

        except Exception as e:
            # 获取⼊参失败时，抛出错误码及错误信息
            http_response(self, ERROR_CODE['3001'], '3001')
            print(f"ERROR： {e}")


# class GetHandler(BaseHandler):
#     def get(self):
#         try:
#             # 获取⼊参
#             questionnaire_id = self.get_argument('questionnaireId')
#             _type = self.get_argument('type')
#             question = self.get_argument('question')
#             options = self.get_argument('options')
#             options_count = self.get_argument('options_count')
#
#             question = Questions(questionnaireId=questionnaire_id, type=_type, question=question, options=options,
#                                  options_count=options_count)
#             code = question.add()
#             http_response(self, ERROR_CODE[code], code)
#
#         except Exception as e:
#             # 获取⼊参失败时，抛出错误码及错误信息
#             http_response(self, ERROR_CODE['3001'], '3001')
#             print(f"ERROR： {e}")
