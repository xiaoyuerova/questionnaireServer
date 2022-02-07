from common.models import RespondentsBase
from conf.base import (
    ERROR_CODE,
    QUESTION_TYPE,
    QUESTION_LEN_MAX,
    QUESTION_LEN_MIN,
    OPTIONS_LEN_MAX,
    OPTIONS_LEN_MIN
)

from common.db.questionnaires import query_questionnaires

from conf.base import Session
from sqlalchemy.orm import scoped_session


class Respondents(RespondentsBase):
    def __init__(self, **kwargs):
        questionnaire_id = kwargs['questionnaireId']
        if type(questionnaire_id) == str:
            questionnaire_id = int(questionnaire_id)
        super(Respondents, self).__init__(questionnaire_id)

    def verify(self):
        """
        在像数据库添加数据前，检查各个数据是否有问题
        :return: 状态码
        """
        questionnaire = query_questionnaires(self.questionnaireId, key='id')
        if not questionnaire:
            return '4002'
        return '0'

    def add(self):
        """
        向数据库添加注册答题人
        :return: 状态码
        """
        code = self.verify()
        if code != '0':
            print(ERROR_CODE[code])
            return code
        session = scoped_session(Session)
        try:
            session.add(self)
            session.commit()
            print('add successful')
            return '0'
        except Exception as e:
            session.rollback()
            print(f"ERROR： {e}")
        finally:
            session.close()
