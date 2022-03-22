from common.db.questions import Questions, query_questions
from common.db.answers import Answers
from common.db.questionnaires import Questionnaires, query_questionnaires


def complete_handler(answers_obj: list[Answers], de_complete=False):
    """
    完成问卷作答后，进行数据统计，并将这份问卷答案标记为已完成。或者是其逆过程，即想要修改以锁定的答案
    :param answers_obj: 数据库保存的答案
    :param de_complete: 解锁
    :return:
    """
    questionnaire: Questionnaires = query_questionnaires(answers_obj[0].questionnaireId, key='id')
    if not de_complete:
        questionnaire.modify(questionnaire.respondentsCount + 1, key='respondentsCount')
    else:
        questionnaire.modify(questionnaire.respondentsCount - 1, key='respondentsCount')
    for answer_obj in answers_obj:
        question: Questions = query_questions(answer_obj.questionId, key='id')
        for i in range(0, len(answer_obj.answer)):
            if answer_obj.answer[i]:
                if not de_complete:
                    question.referenceAnswer[i] += 1
                else:
                    question.referenceAnswer[i] -= 1
        question.modify(question.referenceAnswer)
