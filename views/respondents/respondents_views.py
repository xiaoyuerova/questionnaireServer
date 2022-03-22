from common.BaseHandler import BaseHandler
from common.db.respondents import Respondents, query_respondents
from common.db.questionnaires import query_questionnaires
from common.db.questions import query_questions
from common.db.answers import query_answers
from common.db.delete import delete_respondents
from views.respondents.utils import complete_handler

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
            # 验证
            if not respondent:
                http_response(self, ERROR_CODE['4003'], '4003')
                return
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
