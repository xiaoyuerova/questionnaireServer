from common.models import AnswersBase
from conf.base import (
    ERROR_CODE
)

from conf.base import Session
from sqlalchemy.orm import scoped_session

from common.db.questions import query_questions


class Answers(AnswersBase):
    def __init__(self, **kwargs):
        respondent_id = kwargs.get('respondentId')
        questionnaire_id = kwargs.get('questionnaireId')
        question_id = kwargs.get('questionId')
        reference = kwargs.get('reference')
        reference_answer = kwargs.get('referenceAnswer')
        answer = kwargs.get('answer')
        reference_text_answer = kwargs.get('referenceTextAnswer')
        text_answer = kwargs.get('textAnswer')
        if type(respondent_id) == str:
            respondent_id = int(respondent_id)
        if type(questionnaire_id) == str:
            questionnaire_id = int(questionnaire_id)
        if type(question_id) == str:
            question_id = int(question_id)
        if type(reference_answer) == list:
            reference_answer = str(reference_answer)
        if type(answer) == list:
            answer = str(answer)

        super(Answers, self).__init__(respondent_id, questionnaire_id, question_id, reference, reference_answer, answer,
                                      reference_text_answer, text_answer)

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

    def modify(self, value, key='answer'):
        if not value:
            return '5006'
        session = scoped_session(Session)
        try:
            if key == 'answer':
                if type(value) == list:
                    value = str(value)
                session.query(Answers).filter(Answers.id == self.id).update({Answers.answer: value})
            session.commit()
            print('modify successful')
            return '0'
        except Exception as e:
            session.rollback()
            print(f"ERROR： {e}")
        finally:
            session.close()

    # def check(self):
    #     ex_a = query_answers(self.id, key='id')
    #     if not ex_a:
    #         return '5020'
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
                return check_out(ex_as)
            if key == 'id':
                ex_as = session.query(Answers).filter(Answers.id == value).all()
                return check_out(ex_as)
            if key == 'respondentId':
                ex_as = session.query(Answers).filter(Answers.respondentId == value).all()
                return check_out(ex_as)
            return
        if key == 'questionnaireId':
            ex_a = session.query(Answers).filter(Answers.questionnaireId == value).first()
            return check_out([ex_a])[0]
        if key == 'id':
            ex_a = session.query(Answers).filter(Answers.id == value).first()
            return check_out([ex_a])[0]
        if key == 'respondentId':
            ex_a = session.query(Answers).filter(Answers.respondentId == value).first()
            return check_out([ex_a])[0]
        print(ERROR_CODE['1'])
        return
    except Exception as e:
        session.rollback()
        print(f"ERROR： {e}")
    finally:
        session.close()


def check_out(answers: list[Answers]):
    for answer in answers:
        answer.referenceAnswer = eval(answer.referenceAnswer)
        answer.answer = eval(answer.answer)
    return answers
