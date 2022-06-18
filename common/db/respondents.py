from common.models import RespondentsBase
from conf.base import (
    ERROR_CODE
)

from common.db.questionnaires import query_questionnaires

from conf.base import Session
from sqlalchemy.orm import scoped_session


def query_respondents(value, key='id', search_all=False):
    """
    :param value: 要搜索的值
    :param key: 要搜索的属性
    :param search_all: True表示搜索全部匹配值，False表示只获取第一个匹配值
    :return:
    """
    session = scoped_session(Session)
    try:
        if search_all:
            if key == 'id':
                ex_rs = session.query(Respondents).filter(Respondents.id == value).all()
                return ex_rs
            if key == 'questionnaireId':
                ex_rs = session.query(Respondents).filter(Respondents.questionnaireId == value).all()
                return ex_rs
            return
        if key == 'id':
            ex_r = session.query(Respondents).filter(Respondents.id == value).first()
            return ex_r
        if key == 'questionnaireId':
            ex_r = session.query(Respondents).filter(Respondents.questionnaireId == value).first()
            return ex_r
        print(ERROR_CODE['1'])
        return
    except Exception as e:
        session.rollback()
        print(f"ERROR： {e}")
    finally:
        session.close()


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

    def modify(self, value, key='complete'):
        if not value:
            return '4010'
        session = scoped_session(Session)
        try:
            if key == 'complete':
                session.query(Respondents).filter(Respondents.id == self.id).update({Respondents.complete: value})
            session.commit()
            print('modify successful')
            return '0'
        except Exception as e:
            session.rollback()
            print(f"ERROR： {e}")
        finally:
            session.close()
