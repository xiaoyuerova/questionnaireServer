from common.models import QuestionnairesBase
from conf.base import (
    QUESTIONNAIRE_NAME_LEN_MIN,
    QUESTIONNAIRE_NAME_LEN_MAX,
    ERROR_CODE
)

from conf.base import Session
from sqlalchemy.orm import scoped_session

from common.db.questioners import query_questioners


def query_questionnaires(value, key='name', search_all=False):
    """
    :param value: 要搜索的值
    :param key: 要搜索的属性
    :param search_all: True表示搜索全部匹配值，False表示只获取第一个匹配值
    :return:
    """
    session = scoped_session(Session)
    try:
        if search_all:
            if key == 'name':
                ex_qs = session.query(Questionnaires).filter(Questionnaires.name == value).all()
                return ex_qs
            if key == 'id':
                ex_qs = session.query(Questionnaires).filter(Questionnaires.id == value).all()
                return ex_qs
            return
        if key == 'name':
            ex_q = session.query(Questionnaires).filter(Questionnaires.name == value).first()
            return ex_q
        if key == 'id':
            ex_q = session.query(Questionnaires).filter(Questionnaires.id == value).first()
            return ex_q
        return
    except Exception as e:
        session.rollback()
        print(f"ERROR： {e}")
    finally:
        session.close()


class Questionnaires(QuestionnairesBase):
    def __init__(self, **kwargs):
        """
        questionerId: str 或 int
        name: str
        :param kwargs:
        """
        questioner_id = kwargs['questionerId']
        name = kwargs['name']
        if type(questioner_id) == str:
            questioner_id = int(questioner_id)
        super(Questionnaires, self).__init__(questioner_id, name)

    def verify(self):
        if len(self.name) < QUESTIONNAIRE_NAME_LEN_MIN:
            return '2002'
        if len(self.name) > QUESTIONNAIRE_NAME_LEN_MAX:
            return '2003'
        questioner = query_questioners(self.questionerId, key='id')
        if questioner:
            return '0'
        return '2004'

    def add(self):
        code = self.verify()
        if code != '0':
            print(ERROR_CODE[code])
            return code
        session = scoped_session(Session)
        try:
            ex_q = query_questionnaires(self.name)
            if ex_q:
                print(ERROR_CODE['2005'])
                return '2005'
            else:
                session.add(self)
                session.commit()
                print('add successful')
                return '0'
        except Exception as e:
            session.rollback()
            print(f"ERROR： {e}")
        finally:
            session.close()
