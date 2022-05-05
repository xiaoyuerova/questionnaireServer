from common.BaseHandler import BaseHandler
import json
from common.db.answers import Answers
from common.decorated import respondent_auth

from conf.base import (
    ERROR_CODE
)

from common.commons import http_response
from common.db.respondents import query_respondents
from common.db.questionnaires import query_questionnaires
from common.db.answers import query_answers
from common.db.delete import delete_answers


class SubmitHandler(BaseHandler):
    @respondent_auth
    def post(self):
        """
        提交答案
        answers: [
            {'questionId':id,'reference': ,'referenceAnswer':[],'answer':[]}
        ]
        :return:
        """
        try:
            # 获取⼊参
            respondent_id = self.get_argument('respondentId')
            questionnaire_id = self.get_argument('questionnaireId')
            answers = self.get_argument('answers')
            # 验证答题人身份
            respondent = query_respondents(respondent_id, key='id')
            if not respondent:
                http_response(self, ERROR_CODE['5002'], '5002')
                return
            # 验证问卷是否存在
            questionnaire = query_questionnaires(questionnaire_id, key='id')
            if not questionnaire:
                http_response(self, ERROR_CODE['5005'], '5005')
                return
            answers = json.loads(answers)
            if answers:
                ex_as = query_answers(respondent_id, key='respondentId', search_all=True)
                for answer in answers:
                    # 检查提交答案题目，数据库中是否已经存在答案，存在就修改，不存在添加
                    flag = True
                    index = 0
                    if ex_as:
                        for i in range(0, len(ex_as)):
                            if answer['questionId'] == ex_as[i].questionId:
                                flag = False
                                index = i
                                break
                    if flag:
                        # 向数据库添加一个answer，同时修改对应问题的referenceAnswer（回答统计信息）
                        answer_obj = Answers(respondentId=respondent_id,
                                             questionnaireId=questionnaire_id,
                                             questionId=answer['questionId'],
                                             reference=answer['reference'],
                                             referenceAnswer=answer['referenceAnswer'],
                                             answer=answer['answer'])
                        answer_obj.add()
                        # question = query_questions(answer_obj.questionId, key='id')
                        # temp_reference_answer = eval(question.referenceAnswer)
                        # new_answer = eval(answer_obj.answer)
                        # for i in range(0, len(new_answer)):
                        #     if new_answer[i]:
                        #         temp_reference_answer[i] += 1
                        # question.modify(str(temp_reference_answer), key='referenceAnswer')

                    else:
                        # 数据库中已经存在回答，先修改对应问题的referenceAnswer（回答统计信息）,再修改answers
                        new_answer = answer['answer']
                        if type(new_answer) == str:
                            new_answer = eval(new_answer)
                        # question = query_questions(answer['questionId'], key='id')
                        # temp_reference_answer = eval(question.referenceAnswer)
                        # for i in range(0, len(old_answer)):
                        #     if old_answer[i]:
                        #         temp_reference_answer[i] -= 1
                        # for i in range(0, len(new_answer)):
                        #     if new_answer[i]:
                        #         temp_reference_answer[i] += 1
                        # question.modify(str(temp_reference_answer), key='referenceAnswer')
                        ex_as[index].modify(str(new_answer))
            http_response(self, ERROR_CODE['0'], '0')

        except Exception as e:
            # 获取⼊参失败时，抛出错误码及错误信息
            http_response(self, ERROR_CODE['5001'], '5001')
            print(f"ERROR： {e}")


class DeleteHandler(BaseHandler):
    def post(self):
        try:
            # 获取⼊参
            ids = self.get_argument('answerIds')

            if type(ids) == str:
                ids = eval(ids)
            code = delete_answers(ids)
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
