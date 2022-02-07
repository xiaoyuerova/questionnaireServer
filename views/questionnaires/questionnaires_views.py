from common.BaseHandler import BaseHandler
from common.db.questionnaires import Questionnaires, query_questionnaires
from common.db.questions import query_questions
from common.commons import list_to_dict, option_parsing
import json

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
            http_response(self, ERROR_CODE[code], code)

        except Exception as e:
            # 获取⼊参失败时，抛出错误码及错误信息
            http_response(self, ERROR_CODE['2001'], '2001')
            print(f"ERROR:{e}")


class GetHandler(BaseHandler):
    def get(self):
        try:
            # 获取参数
            questionnaire_id = self.get_argument('questionnaireId')

            questionnaire = query_questionnaires(questionnaire_id, key='id')
            if questionnaire:
                questions_obj = query_questions(questionnaire_id, search_all=True)
                data = []
                for item in questions_obj:
                    item.options = option_parsing(item.options)
                    dict_ = item.__dict__
                    del dict_['_sa_instance_state']
                    data.append(json.dumps(dict_))
                print(data)
                http_response(self, data, '0')
            else:
                http_response(self, ERROR_CODE['2006'], '2006')

        except Exception as e:
            # 获取⼊参失败时，抛出错误码及错误信息
            http_response(self, ERROR_CODE['2001'], '2001')
            print(f"ERROR:{e}")
