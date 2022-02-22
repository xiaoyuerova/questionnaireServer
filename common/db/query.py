from conf.base import (
    ERROR_CODE
)

from conf.base import Session
from sqlalchemy.orm import scoped_session
from common.db.questioners import Questioners
from common.db.questionnaires import Questionnaires
from common.db.questions import Questions
from common.db.respondents import Respondents
from common.db.answers import Answers


def query_questioners(value, key='userName', search_all=False):
    """
    :param value: 要搜索的值
    :param key: 要搜索的属性
    :param search_all: True表示搜索全部匹配值，False表示只获取第一个匹配值
    :return:
    """
    session = scoped_session(Session)
    try:
        if search_all:
            if key == 'userName':
                ex_qs = session.query(Questioners).filter(Questioners.userName == value).all()
                return ex_qs
            if key == 'id':
                ex_qs = session.query(Questioners).filter(Questioners.id == value).all()
                return ex_qs
            if key == 'email':
                ex_qs = session.query(Questioners).filter(Questioners.email == value).all()
                return ex_qs
            return
        if key == 'userName':
            ex_q = session.query(Questioners).filter(Questioners.userName == value).first()
            return ex_q
        if key == 'id':
            ex_q = session.query(Questioners).filter(Questioners.id == value).first()
            return ex_q
        if key == 'email':
            ex_q = session.query(Questioners).filter(Questioners.email == value).first()
            return ex_q
        print(ERROR_CODE['1'])
        return
    except Exception as e:
        session.rollback()
        print(f"ERROR： {e}")
    finally:
        session.close()


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
            return
        if key == 'id':
            ex_r = session.query(Respondents).filter(Respondents.id == value).first()
            return ex_r
        print(ERROR_CODE['1'])
        return
    except Exception as e:
        session.rollback()
        print(f"ERROR： {e}")
    finally:
        session.close()


def query_answers(value, key='questionnaireId', search_all=False):
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
                ex_as = session.query(Answers).filter(Answers.questionnaireId == value).all()
                return ex_as
            if key == 'id':
                ex_as = session.query(Answers).filter(Answers.id == value).all()
                return ex_as
            if key == 'respondentId':
                ex_as = session.query(Answers).filter(Answers.respondentId == value).all()
                return ex_as
            return
        if key == 'questionnaireId':
            ex_a = session.query(Answers).filter(Answers.questionnaireId == value).first()
            return ex_a
        if key == 'id':
            ex_a = session.query(Answers).filter(Answers.id == value).first()
            return ex_a
        if key == 'respondentId':
            ex_a = session.query(Answers).filter(Answers.respondentId == value).first()
            return ex_a
        print(ERROR_CODE['1'])
        return
    except Exception as e:
        session.rollback()
        print(f"ERROR： {e}")
    finally:
        session.close()
