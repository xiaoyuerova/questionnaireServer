from common.models import QuestionnairesBase
from conf.base import (
    QUESTIONNAIRE_NAME_LEN_MIN,
    QUESTIONNAIRE_NAME_LEN_MAX,
    ERROR_CODE
)

from conf.base import Session
from sqlalchemy.orm import scoped_session
# 防止循环调用说明：排序questioners、questionnaires、questions、respondents、answers。这5个模块间的调用只允许排序在前的调用后面的。
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
            if key == 'questionerId':
                ex_qs = session.query(Questionnaires).filter(Questionnaires.questionerId == value).all()
                return ex_qs
            return
        if key == 'name':
            ex_q = session.query(Questionnaires).filter(Questionnaires.name == value).first()
            return ex_q
        if key == 'id':
            ex_q = session.query(Questionnaires).filter(Questionnaires.id == value).first()
            return ex_q
        if key == 'questionerId':
            ex_q = session.query(Questionnaires).filter(Questionnaires.questionerId == value)
            return ex_q
        print(ERROR_CODE['1'])
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
        model: int
        :param kwargs:
        """
        questioner_id = kwargs.get('questionerId')
        name = kwargs.get('name')
        model = kwargs.get('model')
        super(Questionnaires, self).__init__(questioner_id, name, model)

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

    def modify(self, value, key='name'):
        if not value:
            return '2010'
        session = scoped_session(Session)
        try:
            if key == 'name':
                session.query(Questionnaires).filter(Questionnaires.id == self.id).update({Questionnaires.name: value})
            if key == 'published':
                session.query(Questionnaires).filter(Questionnaires.id == self.id).update(
                    {Questionnaires.published: value})
            if key == 'respondentsCount':
                session.query(Questionnaires).filter(Questionnaires.id == self.id).update(
                    {Questionnaires.respondentsCount: value})
            session.commit()
            print('modify successful')
            return '0'
        except Exception as e:
            session.rollback()
            print(f"ERROR： {e}")
        finally:
            session.close()

    # def check(self):
    #     ex_questionnaire = query_questionnaires(self.id, key='id')
    #     if not ex_questionnaire:
    #         return '2020'
    #     # 删除本问卷包含的问题信息（questions）
    #     ex_qs = query_questions(self.id, search_all=True)
    #     if ex_qs:
    #         for ex_q in ex_qs:
    #             ex_q.delete()
    #     # 删除本问卷包含的答案，答题人信息（answers，respondents）,删除respondents时会同时删除依赖的answers
    #     ex_rs = query_respondents(self.id, key='questionnaireId', search_all=True)
    #     if ex_rs:
    #         for ex_r in ex_rs:
    #             ex_r.delete()
    #     return '0'
    #
    # def delete(self):
    #     code = self.check()
    #     if code != '0':
    #         print(ERROR_CODE[code])
    #         return code
    #     session = scoped_session(Session)
    #     try:
    #         session.delete(self)
    #         session.commit()
    #         print('delete successful')
    #         return '0'
    #     except Exception as e:
    #         session.rollback()
    #         print(f"ERROR： {e}")
    #     finally:
    #         session.close()
