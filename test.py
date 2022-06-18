from common.db import Questioners, Questionnaires, Questions, RespondentsSummer


def init_questioner():
    beans = {
        'user_name': 'test_man',
        'email': 'test@123.com',
        'password': '123456',
    }
    q = Questioners(**beans)
    q.add()


def init_questionnaire(questioner_id, name, model):
    bean = {
        'questionerId': questioner_id,
        'name': name,
        'model': model
    }
    q = Questionnaires(**bean)
    q.add()


# beans = {
#         'questionnaireId': None,
#         'questionNumber': None,
#         'type': None,
#         'model': None,
#         'question': None,
#         'options': None,
#         'optionsCount': None,
#         'referenceText': None
#     }


def add_question():
    beans = {
        'questionnaireId': 1,
        'questionNumber': 1,
        'type': 0,
        'model': 1,
        'question': '您晚上休息的时间是在：',
        'options': "['10:00之前','10:00---12:00','12:00---1:00','1:00-2:00','2:00以后','休息是该在晚上干的事吗？']",
        'optionsCount': 6,
        'referenceText': None
    }
    q = Questions(**beans)
    q.add()


def main():
    init_questioner()
    init_questionnaire(1, '熬夜情况调研', 0)
    add_question()


if __name__ == "__main__":
    main()
