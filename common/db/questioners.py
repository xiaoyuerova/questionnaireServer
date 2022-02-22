from common.models import QuestionersBase
from conf.base import (
    USER_NAME_LEN_MAX,
    USER_NAME_LEN_MIN,
    PWD_LEN_MIN,
    PWD_LEN_MAX,
    ERROR_CODE
)

from conf.base import Session
from sqlalchemy.orm import scoped_session


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


class Questioners(QuestionersBase):
    def __init__(self, **kwargs):
        user_name = kwargs['user_name']
        email = kwargs['email']
        password = kwargs['password']
        super(Questioners, self).__init__(user_name, email, password)

    def verify(self):
        if len(self.userName) < USER_NAME_LEN_MIN:
            return '1002'
        if len(self.userName) > USER_NAME_LEN_MAX:
            return '1003'
        if len(self.password) < PWD_LEN_MIN:
            return '1004'
        if len(self.password) > PWD_LEN_MAX:
            return '1005'
        return '0'

    def add(self):
        code = self.verify()
        if code != '0':
            print(ERROR_CODE[code])
            return code
        session = scoped_session(Session)
        try:
            ex_q = session.query(Questioners).filter(Questioners.userName == self.userName).first()
            if ex_q:
                print(ERROR_CODE['1006'])
                return '1006'
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

    # def check(self):
    #     ex_questioner = query_questioners(self.id, key='id')
    #     if not ex_questioner:
    #         return '1020'
    #     # 删除依赖该用户的问卷
    #     ex_qs = query_questionnaires(self.id, key='questionerId', search_all=True)
    #     if ex_qs:
    #         for ex_q in ex_qs:
    #             ex_q.delete()
    #     return '0'
    #
    # def delete(self):
    #     # code = self.check()
    #     # if code != '0':
    #     #     print(ERROR_CODE[code])
    #     #     return code
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
