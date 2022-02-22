from common.models import QuestionsBase
from conf.base import (
    ERROR_CODE,
    QUESTION_TYPE,
    QUESTION_LEN_MAX,
    QUESTION_LEN_MIN,
    OPTIONS_LEN_MAX,
    OPTIONS_LEN_MIN
)
from common.commons import option_parsing

from conf.base import Session
from sqlalchemy.orm import scoped_session

from common.db.questionnaires import query_questionnaires


def query_questions(value, key='questionnaireId', search_all=False):
    """
    :param value: 要搜索的值
    :param key: 要搜索的属性
    :param search_all: True表示搜索全部匹配值，False表示只获取第一个匹配值
    :return:
    """
    session = scoped_session(Session)
    try:
        if search_all:
            if key == 'questionnaireId':
                ex_qs = session.query(Questions).filter(Questions.questionnaireId == value).all()
                return ex_qs
            if key == 'id':
                ex_qs = session.query(Questions).filter(Questions.id == value).all()
                return ex_qs
            return
        if key == 'questionnaireId':
            ex_q = session.query(Questions).filter(Questions.name == value).first()
            return ex_q
        if key == 'id':
            ex_q = session.query(Questions).filter(Questions.id == value).first()
            return ex_q
        print(ERROR_CODE['1'])
        return
    except Exception as e:
        session.rollback()
        print(f"ERROR： {e}")
    finally:
        session.close()


class Questions(QuestionsBase):
    def __init__(self, **kwargs):
        """
        :param kwargs:
        """
        questionnaire_id = kwargs['questionnaireId']
        question_number = kwargs['questionNumber']
        _type = kwargs['type']
        question = kwargs['question']
        options = kwargs['options']
        options_count = kwargs['optionsCount']
        if type(questionnaire_id) == str:
            questionnaire_id = int(questionnaire_id)
        if type(question_number) == str:
            question_number = int(question_number)
        if type(_type) == str:
            _type = int(_type)
        if type(options_count) == str:
            options_count = int(options_count)
        super(Questions, self).__init__(questionnaire_id, question_number, _type, question, options, options_count)

    def verify(self):
        """
        在像数据库添加数据前，检查各个数据是否有问题
        :return: 状态码
        """
        questionnaire = query_questionnaires(self.questionnaireId, key='id')
        if not questionnaire:
            return '3002'
        if self.type < 0 or self.type > (len(QUESTION_TYPE) - 1):
            return '3003'
        if len(self.question) < QUESTION_LEN_MIN:
            return '3004'
        if len(self.question) > QUESTION_LEN_MAX:
            return '3005'
        if len(self.options) < OPTIONS_LEN_MIN:
            return '3006'
        if len(self.options) > OPTIONS_LEN_MAX:
            return '3007'
        options_p = option_parsing(self.options)
        if len(options_p) != self.optionsCount:
            return '3008'
        if questionnaire:
            questions = query_questions(self.questionnaireId, key='questionnaireId', search_all=True)
            for question in questions:
                if question.questionNumber == self.questionNumber:
                    return '3009'
        return '0'

    def add(self):
        """
        给问卷添加题目
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

    def modify(self, value, key='referenceAnswer'):
        if not value:
            return '3010'
        session = scoped_session(Session)
        try:
            if key == 'referenceAnswer':
                session.query(Questions).filter(Questions.id == self.id).update({Questions.referenceAnswer: value})
            if key == 'reference':
                session.query(Questions).filter(Questions.id == self.id).update({Questions.reference: value})
            session.commit()
            print('modify successful')
            return '0'
        except Exception as e:
            session.rollback()
            print(f"ERROR： {e}")
        finally:
            session.close()
