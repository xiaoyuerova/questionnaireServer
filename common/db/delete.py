from conf.base import Session
from sqlalchemy.orm import scoped_session

from conf.base import ERROR_CODE

from common.db.questioners import Questioners, query_questioners
from common.db.questionnaires import Questionnaires, query_questionnaires
from common.db.questions import Questions, query_questions
from common.db.respondents import Respondents, query_respondents
from common.db.answers import Answers, query_answers


def delete_questioners(questioner_ids):
    """
    删除数据
    :param questioner_ids: 要删除questioner的id列表
    :return: 状态码code, 数据(未查询到数据的id，即删除失败的id)
    """
    try:
        if not questioner_ids:
            return '1021', ERROR_CODE['1021']
        session = scoped_session(Session)
        try:
            # 删除questioners
            error_ids = []
            error_flag = False
            for id_ in questioner_ids:
                questioner = query_questioners(id_, key='id')
                if questioner:
                    delete_flag = False
                    # 删除这位用户的所有问卷
                    questionnaires = query_questionnaires(questioner.questionnaireId, key='id', search_all=True)
                    if questionnaires:
                        questionnaire_ids = []
                        for questionnaire in questionnaires:
                            questionnaire_ids.append(questionnaire.id)
                        code = delete_questionnaires(questionnaire_ids)
                        if code == '0':
                            delete_flag = True
                        else:
                            code, error_ = code
                            print(ERROR_CODE[code],code)
                    else:
                        delete_flag = True
                    if delete_flag:
                        session.delete(questioner)
                    else:
                        print('debug delete_questioners中questionnaire外键依赖数据删除失败')
                        error_ids.append(id_)
                        error_flag = True
                else:
                    error_ids.append(id_)
                    error_flag = True
            session.commit()
            print('delete complete')
            if error_flag:
                return '1022', error_ids
            return '0'
        except Exception as e:
            session.rollback()
            print(f"ERROR： {e}")
        finally:
            session.close()

    except Exception as e:
        # 运行出错，抛出错误码及错误信息
        print(f"ERROR： {e}")


def delete_questionnaires(questionnaire_ids):
    try:
        if not questionnaire_ids:
            return '2021', ERROR_CODE['2021']
        session = scoped_session(Session)
        try:
            # 删除questionnaires。先删除外键依赖的数据。依次是answers、respondents、questions
            error_ids = []
            error_flag = False
            for id_ in questionnaire_ids:
                questionnaire = query_questionnaires(id_, key='id')
                if questionnaire:
                    delete_flag1 = False
                    delete_flag2 = False
                    delete_flag3 = False
                    # 删除所有答案信息
                    answers = query_answers(questionnaire.id, key='questionnaireId', search_all=True)
                    if answers:
                        answers_ids = []
                        for answer in answers:
                            answers_ids.append(answer.id)
                        code = delete_answers(answers_ids)
                        if code == '0':
                            delete_flag1 = True
                        else:
                            code, error_ = code
                            print(ERROR_CODE[code],code)
                    else:
                        print('没有answers了')
                        delete_flag1 = True

                    if delete_flag1:
                        # 继续删除respondents、questions
                        # 删除问卷的所有答题人信息
                        respondents = query_respondents(questionnaire.id, key='questionnaireId', search_all=True)
                        if respondents:
                            respondent_ids = []
                            for respondent in respondents:
                                respondent_ids.append(respondent.id)
                            code = delete_respondents(respondent_ids)
                            if code == '0':
                                delete_flag2 = True
                            else:
                                code, error_ = code
                                print(ERROR_CODE[code], code)
                        else:
                            print('没有respondents了')
                            delete_flag2 = True
                        # 删除问卷的所有问题
                        questions = query_questions(questionnaire.id, key='questionnaireId', search_all=True)
                        if questions:
                            question_ids = []
                            for question in questions:
                                question_ids.append(question.id)
                            code = delete_questions(question_ids)
                            if code == '0':
                                delete_flag3 = True
                            else:
                                code, error_ = code
                                print(ERROR_CODE[code], code)
                        else:
                            print('没有questions了')
                            delete_flag3 = True

                        # 确认没有外键依赖数据，删除问卷
                        if delete_flag2 and delete_flag3:
                            session.delete(questionnaire)
                        else:
                            print('debug delete_questionnaires中question或respondents外键依赖数据删除失败')
                            error_ids.append(id_)
                            error_flag = True
                    else:
                        error_ids.append(id_)
                        error_flag = True
                else:
                    error_ids.append(id_)
                    error_flag = True
            session.commit()
            print('delete complete')
            if error_flag:
                return '2022', error_ids
            return '0'
        except Exception as e:
            session.rollback()
            print(f"ERROR： {e}")
        finally:
            session.close()

    except Exception as e:
        # 运行出错，抛出错误码及错误信息
        print(f"ERROR： {e}")


def delete_questions(question_ids):
    try:
        if not question_ids:
            return '3021', ERROR_CODE['3021']
        session = scoped_session(Session)
        try:
            # 删除questions
            error_ids = []
            error_flag = False
            for id_ in question_ids:
                question = query_questions(id_, key='id')
                if question:
                    session.delete(question)
                else:
                    error_ids.append(id_)
                    error_flag = True
            session.commit()
            print('delete complete')
            if error_flag:
                return '3022', error_ids
            return '0'
        except Exception as e:
            session.rollback()
            print(f"ERROR： {e}")
        finally:
            session.close()

    except Exception as e:
        # 运行出错，抛出错误码及错误信息
        print(f"ERROR： {e}")


def delete_respondents(respondent_ids):
    try:
        if not respondent_ids:
            return '4021', ERROR_CODE['4021']
        session = scoped_session(Session)
        try:
            # 删除questions
            error_ids = []
            error_flag = False
            for id_ in respondent_ids:
                respondent = query_respondents(id_, key='id')
                if respondent:
                    delete_flag = False
                    # 删除答题人的所有答案信息
                    answers = query_answers(respondent.id, key='respondentId', search_all=True)
                    if answers:
                        answer_ids = []
                        for answer in answers:
                            answer_ids.append(answer.id)
                        code = delete_answers(answer_ids)
                        if code == '0':
                            delete_flag = True
                        else:
                            code, error_ = code
                            print(ERROR_CODE[code], code)
                    else:
                        delete_flag = True
                    # 删除答题人信息
                    if delete_flag:
                        # 删除前修改参与问卷人数
                        if respondent.complete:
                            questionnaire = query_questionnaires(respondent.questionnaireId, key='id')
                            questionnaire.modify(questionnaire.respondentsCount - 1, key='respondentsCount')
                        session.delete(respondent)
                    else:
                        error_ids.append(id_)
                        error_flag = True
                else:
                    error_ids.append(id_)
                    error_flag = True
            session.commit()
            print('delete complete')
            if error_flag:
                return '4022', error_ids
            return '0'
        except Exception as e:
            session.rollback()
            print(f"ERROR： {e}")
        finally:
            session.close()

    except Exception as e:
        # 运行出错，抛出错误码及错误信息
        print(f"ERROR： {e}")


def delete_answers(answer_ids):
    try:
        if not answer_ids:
            return '5021', ERROR_CODE['5021']
        session = scoped_session(Session)
        try:
            # 删除answers
            error_ids = []
            error_flag = False
            for id_ in answer_ids:
                answer = query_answers(id_, key='id')
                if answer:
                    session.delete(answer)
                else:
                    error_ids.append(id_)
                    error_flag = True
            session.commit()
            print('delete complete')
            if error_flag:
                return '5022', error_ids
            return '0'
        except Exception as e:
            session.rollback()
            print(f"ERROR： {e}")
        finally:
            session.close()

    except Exception as e:
        # 运行出错，抛出错误码及错误信息
        print(f"ERROR： {e}")
