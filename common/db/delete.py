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
                    # 删除这位用户的所有问卷
                    questionnaires = query_questionnaires(questioner.questionnaireId, key='id', search_all=True)
                    if questionnaires:
                        questionnaire_ids = []
                        for questionnaire in questionnaires:
                            questionnaire_ids.append(questionnaire.id)
                            delete_questionnaires(questionnaire_ids)
                    session.delete(questioner)
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
            # 删除questionnaires
            error_ids = []
            error_flag = False
            for id_ in questionnaire_ids:
                questionnaire = query_questionnaires(id_, key='id')
                if questionnaire:
                    # 删除问卷的所有问题
                    questions = query_questions(questionnaire.id, key='questionnaireId', search_all=True)
                    if questions:
                        question_ids = []
                        for question in questions:
                            question_ids.append(question.id)
                            # delete_questions(question_ids)
                    session.delete(questionnaire)
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


# def delete_questions(question_ids):
#     try:
#         if not question_ids:
#             return '3021', ERROR_CODE['3021']
#         session = scoped_session(Session)
#         try:
#             # 删除questions
#             error_ids = []
#             error_flag = False
#             for id_ in questionnaire_ids:
#                 questionnaire = query_questionnaires(id_, key='id')
#                 if questionnaire:
#                     # 删除问卷的所有问题
#                     questions = query_questions(questionnaire.id, key='questionnaireId', search_all=True)
#                     if questions:
#                         question_ids = []
#                         for question in questions:
#                             question_ids.append(question.id)
#                             delete_questions(question_ids)
#                     session.delete(questionnaire)
#                 else:
#                     error_ids.append(id_)
#                     error_flag = True
#             session.commit()
#             print('delete complete')
#             if error_flag:
#                 return '2022', error_ids
#             return '0'
#         except Exception as e:
#             session.rollback()
#             print(f"ERROR： {e}")
#         finally:
#             session.close()
#
#     except Exception as e:
#         # 运行出错，抛出错误码及错误信息
#         print(f"ERROR： {e}")
