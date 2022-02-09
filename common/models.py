from conf.base import (BaseDB, engine)
from datetime import datetime
import sys
from sqlalchemy import (
    Column,
    Float,
    Integer,
    String,
    Date,
    Time,
    Boolean,
    ForeignKey
)


class QuestionersBase(BaseDB):
    # table for questioners
    __tablename__ = "questioners"
    # 定义表结构
    id = Column(Integer, primary_key=True, autoincrement=True)
    userName = Column(String(50), nullable=False)
    password = Column(String(20), nullable=False)

    def __init__(self, user_name, password):
        self.userName = user_name
        self.password = password


class QuestionnairesBase(BaseDB):
    # table for questionnaires
    __tablename__ = "questionnaires"
    # 定义表结构
    id = Column(Integer, primary_key=True, autoincrement=True)
    questionerId = Column(Integer, ForeignKey("questioners.id"), nullable=False)
    name = Column(String(50), nullable=False)
    date = Column(Date, nullable=False, index=True)
    time = Column(Time, nullable=False, index=True)
    published = Column(Boolean, nullable=False)
    respondentsCount = Column(Integer, nullable=False)

    def __init__(self, questioner_id, name):
        self.questionerId = questioner_id
        self.name = name
        self.date = datetime.now().date()
        self.time = datetime.now().time()
        self.published = False
        self.respondentsCount = 0


class QuestionsBase(BaseDB):
    # table for questions
    __tablename__ = "questions"
    # 定义表结构
    id = Column(Integer, primary_key=True, autoincrement=True)
    questionnaireId = Column(Integer, ForeignKey("questionnaires.id"), nullable=False, index=True)
    type = Column(Integer, nullable=False)
    question = Column(String(2000), nullable=False)
    options = Column(String(1000), nullable=False)
    optionsCount = Column(Integer, nullable=False)

    def __init__(self, questionnaire_id, _type, question, options, options_count):
        self.questionnaireId = questionnaire_id
        self.type = _type
        self.question = question
        self.options = options
        self.optionsCount = options_count


class RespondentsBase(BaseDB):
    # table for respondents
    __tablename__ = "respondents"
    # 定义表结构
    id = Column(Integer, primary_key=True, autoincrement=True)
    questionnaireId = Column(Integer, ForeignKey("questionnaires.id"), nullable=False, index=True)
    date = Column(Date, nullable=False, index=True)
    time = Column(Time, nullable=False, index=True)

    def __init__(self, questionnaire_id):
        self.questionnaireId = questionnaire_id
        self.date = datetime.now().date()
        self.time = datetime.now().time()


class AnswersBase(BaseDB):
    # table for answers
    __tablename__ = "answers"
    # 定义表结构
    id = Column(Integer, primary_key=True, autoincrement=True)
    respondentId = Column(Integer, ForeignKey("respondents.id"), nullable=False, index=True)
    questionnaireId = Column(Integer, ForeignKey("questionnaires.id"), nullable=False, index=True)
    questionId = Column(Integer, ForeignKey("questions.id"), nullable=False, index=True)
    reference = Column(Boolean, nullable=False)
    referenceAnswer = Column(String(1000), nullable=False)
    answer = Column(String(20), nullable=False)

    def __init__(self, respondent_id, questionnaire_id, question_id, reference, reference_answer, answer):
        self.respondentId = respondent_id
        self.questionnaireId = questionnaire_id
        self.questionId = question_id
        self.reference = reference
        self.referenceAnswer = reference_answer
        self.answer = answer


def init_db():
    BaseDB.metadata.create_all(engine)


if __name__ == '__main__':
    print("Initialize database")
    # init_db()
