from common.models import RespondentsSummerBase
from conf.base import (
    ERROR_CODE,
    USER_NAME_LEN_MIN,
    USER_NAME_LEN_MAX,
    PWD_LEN_MIN,
    PWD_LEN_MAX,
)

from conf.base import Session
from sqlalchemy.orm import scoped_session


def query_respondents_summer(value, key='id', search_all=False):
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
                ex_rs = session.query(RespondentsSummer).filter(RespondentsSummer.id == value).all()
                return ex_rs
            if key == 'userName':
                ex_rs = session.query(RespondentsSummer).filter(RespondentsSummer.userName == value).all()
                return ex_rs
            return
        if key == 'id':
            ex_r = session.query(RespondentsSummer).filter(RespondentsSummer.id == value).first()
            return ex_r
        if key == 'userName':
            ex_r = session.query(RespondentsSummer).filter(RespondentsSummer.userName == value).first()
            return ex_r
        print(ERROR_CODE['1'])
        return
    except Exception as e:
        session.rollback()
        print(f"ERROR： {e}")
    finally:
        session.close()


class RespondentsSummer(RespondentsSummerBase):
    def __init__(self, **kwargs):
        user_name = kwargs.get('userName')
        password = kwargs.get('password')

        super(RespondentsSummer, self).__init__(user_name, password)

    def verify(self):
        """
        在像数据库添加数据前，检查各个数据是否有问题
        :return: 状态码
        """
        if len(self.userName) < USER_NAME_LEN_MIN:
            return '6002'
        if len(self.userName) > USER_NAME_LEN_MAX:
            return '6003'
        if len(self.password) < PWD_LEN_MIN:
            return '6004'
        if len(self.password) > PWD_LEN_MAX:
            return '6005'
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

    # def modify(self, value, key=''):
    #     if not value:
    #         return '4010'
    #     session = scoped_session(Session)
    #     try:
    #         if key == 'complete':
    #             session.query(Respondents).filter(Respondents.id == self.id).update({Respondents.complete: value})
    #         session.commit()
    #         print('modify successful')
    #         return '0'
    #     except Exception as e:
    #         session.rollback()
    #         print(f"ERROR： {e}")
    #     finally:
    #         session.close()
