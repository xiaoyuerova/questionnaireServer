from common.BaseHandler import BaseHandler
from common.db import *
from common.commons import list_to_dict, option_parsing
from common.decorated import respondent_auth, respondent_s_auth

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
        # item.options = eval(item.options)
        dict_ = item.__dict__
        del dict_['_sa_instance_state']
        questions.append(dict_)
    return questions


def get_answers(respondent_id):
    answers_obj = query_answers(respondent_id, key='respondentId', search_all=True)
    answers = []
    if answers_obj:
        for item in answers_obj:
            dict_ = item.__dict__
            del dict_['_sa_instance_state']
            answers.append(dict_)
    return answers


class GetHandler(BaseHandler):
    """
    获取问卷信息
    return
        data = {
            'question': ,
            'answer': ,
        }
    """

    @respondent_auth
    def get(self):
        try:
            # 获取参数
            respondent_id = self.user.id
            questionnaire_id = self.user.questionnaireId

            questionnaire = query_questionnaires(questionnaire_id, key='id')
            if questionnaire:
                questionnaire_dict = get_questionnaire(questionnaire)
                questions = get_questions(questionnaire.id)
                answers = get_answers(respondent_id)
                data = {
                    'questionnaire': questionnaire_dict,
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


class DeleteHandler(BaseHandler):
    """
    删除问卷
    """

    def post(self):
        try:
            # 获取⼊参
            ids = self.get_argument('questionnaireIds')

            if type(ids) == str:
                ids = eval(ids)
            code = delete_questionnaires(ids)
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


class SummerGetHandler(BaseHandler):
    """
    获取问卷信息
    return
        data = {
            'question': ,
            'answer': ,
        }
    """
    @respondent_s_auth
    def get(self):
        try:
            # 获取参数
            respondent_id = self.user.id
            questionnaire_id = self.get_argument('qid')

            print('questionnaire_id',questionnaire_id)
            questionnaire = query_questionnaires(questionnaire_id, key='id')
            if questionnaire:
                questionnaire_dict = get_questionnaire(questionnaire)
                questions = get_questions(questionnaire.id)
                answers = get_answers(respondent_id)
                data = {
                    'questionnaire': questionnaire_dict,
                    'questions': questions,
                    'answers': answers
                }
                print('data', data)
                http_response(self, data, '0')
            else:
                http_response(self, ERROR_CODE['2006'], '2006')

        except Exception as e:
            # 获取⼊参失败时，抛出错误码及错误信息
            http_response(self, ERROR_CODE['2001'], '2001')
            print(f"ERROR:{e}")
