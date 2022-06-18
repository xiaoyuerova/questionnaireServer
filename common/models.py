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
    email = Column(String(50), nullable=False)
    password = Column(String(20), nullable=False)

    def __init__(self, user_name, email, password):
        self.userName = user_name
        self.email = email
        self.password = password


class QuestionnairesBase(BaseDB):
    # table for questionnaires
    __tablename__ = "questionnaires"
    # 定义表结构
    id = Column(Integer, primary_key=True, autoincrement=True)
    questionerId = Column(Integer, ForeignKey("questioners.id"), nullable=False)
    name = Column(String(50), nullable=False)
    date = Column(Date, nullable=False)
    time = Column(Time, nullable=False)
    published = Column(Boolean, nullable=False)
    respondentsCount = Column(Integer, nullable=False)
    model = Column(Integer)

    def __init__(self, questioner_id, name, model):
        self.questionerId = questioner_id
        self.name = name
        self.date = datetime.now().date()
        self.time = datetime.now().time()
        self.published = False
        self.respondentsCount = 0
        self.model = model


class QuestionsBase(BaseDB):
    # table for questions
    __tablename__ = "questions"
    # 定义表结构
    id = Column(Integer, primary_key=True, autoincrement=True)
    questionnaireId = Column(Integer, ForeignKey("questionnaires.id"), nullable=False)
    questionNumber = Column(Integer, nullable=False)
    type = Column(Integer, nullable=False)
    model = Column(Integer, nullable=False)
    question = Column(String(2000), nullable=False)
    options = Column(String(1000), nullable=False)
    optionsCount = Column(Integer, nullable=False)
    reference = Column(Boolean, nullable=False)
    referenceAnswer = Column(String(50), nullable=False)
    referenceText = Column(String(600))

    def __init__(self, questionnaire_id, question_number, _type, model, question, options, options_count,
                 reference_text):
        self.questionnaireId = questionnaire_id
        self.questionNumber = question_number
        self.type = _type
        self.model = model
        self.question = question
        self.options = options
        self.optionsCount = options_count
        self.reference = True
        reference_answer = [0] * options_count
        self.referenceAnswer = str(reference_answer)
        self.referenceText = reference_text


class RespondentsBase(BaseDB):
    # table for respondents
    __tablename__ = "respondents"
    # 定义表结构
    id = Column(Integer, primary_key=True, autoincrement=True)
    questionnaireId = Column(Integer, ForeignKey("questionnaires.id"), nullable=False)
    date = Column(Date, nullable=False)
    time = Column(Time, nullable=False)
    complete = Column(Boolean, nullable=False)

    def __init__(self, questionnaire_id):
        self.questionnaireId = questionnaire_id
        self.date = datetime.now().date()
        self.time = datetime.now().time()
        self.complete = False


class AnswersBase(BaseDB):
    # table for answers
    __tablename__ = "answers"
    # 定义表结构
    id = Column(Integer, primary_key=True, autoincrement=True)
    respondentId = Column(Integer, ForeignKey("respondents.id"), nullable=False)
    questionnaireId = Column(Integer, ForeignKey("questionnaires.id"), nullable=False)
    questionId = Column(Integer, ForeignKey("questions.id"), nullable=False)
    reference = Column(Boolean, nullable=False)
    referenceAnswer = Column(String(100))
    answer = Column(String(50))
    referenceTextAnswer = Column(String(600))
    textAnswer = Column(String(600))

    def __init__(self, respondent_id, questionnaire_id, question_id, reference, reference_answer, answer,
                 reference_text_answer, text_answer):
        self.respondentId = respondent_id
        self.questionnaireId = questionnaire_id
        self.questionId = question_id
        self.reference = reference
        self.referenceAnswer = reference_answer
        self.answer = answer
        self.referenceTextAnswer = reference_text_answer
        self.textAnswer = text_answer


class RespondentsSummerBase(BaseDB):
    # table for respondentsSummer
    __tablename__ = "respondentsSummer"
    # 定义表结构
    id = Column(Integer, primary_key=True, autoincrement=True)
    userName = Column(String(50), nullable=False, unique=True)
    password = Column(String(20), nullable=False)

    def __init__(self, user_name, password):
        self.userName = user_name
        self.password = password


def init_db():
    BaseDB.metadata.create_all(engine)


if __name__ == '__main__':
    print("Initialize database")
    # init_db()
