from common.models import AnswersBase
from conf.base import (
    ERROR_CODE
)

from conf.base import Session
from sqlalchemy.orm import scoped_session

from common.db.respondents import query_respondents
from common.db.questions import query_questions


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
        return
    except Exception as e:
        session.rollback()
        print(f"ERROR： {e}")
    finally:
        session.close()


class Answers(AnswersBase):
    def __init__(self, **kwargs):
        respondent_id = kwargs['respondentId']
        questionnaire_id = kwargs['questionnaireId']
        question_id = kwargs['questionId']
        reference = kwargs['reference']
        reference_answer = kwargs['referenceAnswer']
        answer = kwargs['answer']
        if type(respondent_id) == str:
            respondent_id = int(respondent_id)
        if type(questionnaire_id) == str:
            questionnaire_id = int(questionnaire_id)
        if type(question_id) == str:
            question_id = int(question_id)
        if type(reference) == str and reference == 'true':
            reference = True
        if type(reference) == str and reference == 'false':
            reference = False
        super(Answers, self).__init__(respondent_id, questionnaire_id, question_id, reference, reference_answer, answer)

    def verify(self):
        question = query_questions(self.questionId, key='id')
        if not question:
            return '5003'
        return '0'

    def add(self):
        code = self.verify()
        if code != '0':
            print(ERROR_CODE[code])
            return code
        session = scoped_session(Session)
        try:
            ex_as = session.query(Answers).filter(Answers.respondentId == self.respondentId).all()
            for ex_a in ex_as:
                if ex_a.questionId == self.questionId:
                    print(ERROR_CODE['5004'])
                    return '5004'
            session.add(self)
            session.commit()
            print('add successful')
            return '0'
        except Exception as e:
            session.rollback()
            print(f"ERROR： {e}")
        finally:
            session.close()
