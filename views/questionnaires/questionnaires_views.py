from common.BaseHandler import BaseHandler
from common.db.questionnaires import Questionnaires, query_questionnaires
from common.db.questions import query_questions
from common.db.answers import query_answers
from common.commons import list_to_dict, option_parsing
import json
import datetime
from datetime import timedelta

from conf.base import (
    ERROR_CODE
)

from common.commons import http_response


class CreateHandler(BaseHandler):
    """
    创建问卷
    """

    def post(self):
        try:
            # 获取参数
            questioner_id = self.get_argument('questionerId')
            name = self.get_argument('name')

            questionnaire = Questionnaires(questionerId=questioner_id, name=name)
            code = questionnaire.add()
            if code == '0':
                data = {
                    'questionnaireId': questionnaire.id
                }
                http_response(self, data, '0')
            else:
                http_response(self, ERROR_CODE[code], code)

        except Exception as e:
            # 获取⼊参失败时，抛出错误码及错误信息
            http_response(self, ERROR_CODE['2001'], '2001')
            print(f"ERROR:{e}")


def get_questionnaire(questionnaire):
    questionnaire.date = questionnaire.date.strftime("%Y-%m-%d")
    questionnaire.time = questionnaire.time.strftime("%H-%M-%S")
    dict_ = questionnaire.__dict__
    del dict_['_sa_instance_state']
    return dict_


def get_questions(questionnaire_id):
    questions_obj = query_questions(questionnaire_id, search_all=True)
    questions = []
    for item in questions_obj:
        item.options = option_parsing(item.options)
        dict_ = item.__dict__
        del dict_['_sa_instance_state']
        questions.append(dict_)
    return questions


def get_answers(respondent_id):
    answers_obj = query_answers(respondent_id, key='respondentId', search_all=True)
    answers = []
    if answers_obj:
        for item in answers_obj:
            item.referenceAnswer = eval(item.referenceAnswer)
            item.answer = eval(item.answer)
            dict_ = item.__dict__
            del dict_['_sa_instance_state']
            answers.append(dict_)
    return answers


class GetHandler(BaseHandler):
    """
    获取问卷信息
    param respondentId: 答题人id
    param questionnaire_id: 问卷id
    return
        data = {
            'question': ,
            'answer': ,
        }
    """

    def get(self):
        try:
            # 获取参数
            respondent_id = self.get_argument('respondentId')
            questionnaire_id = self.get_argument('questionnaireId')

            questionnaire = query_questionnaires(questionnaire_id, key='id')
            if questionnaire:
                questionnaire_dict = get_questionnaire(questionnaire)
                questions = get_questions(questionnaire.id)
                answers = get_answers(respondent_id)
                data = {
                    'questionnaire': questionnaire.__dict__,
                    'questions': questions,
                    'answers': answers
                }
                http_response(self, data, '0')
            else:
                http_response(self, ERROR_CODE['2006'], '2006')

        except Exception as e:
            # 获取⼊参失败时，抛出错误码及错误信息
            http_response(self, ERROR_CODE['2001'], '2001')
            print(f"ERROR:{e}")
