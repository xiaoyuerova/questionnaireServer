from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('mysql+pymysql://root:wxt123@localhost:3306/questionnaire_sys?charset=utf8', encoding="utf8",
                       echo=False)
BaseDB = declarative_base()
Session = sessionmaker(bind=engine,
                       autocommit=False,
                       autoflush=True,
                       expire_on_commit=False)

# 服务器端 IP+Port
SERVER_PORT = 8010
SERVER_HEADER = "http://127.0.0.1:" + str(SERVER_PORT)
# 用户名长度设定
USER_NAME_LEN_MIN = 1
USER_NAME_LEN_MAX = 40
# 密码长度设定
PWD_LEN_MIN = 6
PWD_LEN_MAX = 18
# 问卷名长度设定
QUESTIONNAIRE_NAME_LEN_MIN = 1
QUESTIONNAIRE_NAME_LEN_MAX = 40
# 题目类型
QUESTION_TYPE = ["单选", "双选", "其它"]
# 选项间隔特殊符号
SPE_CH = '&'
# 题目长度设定
QUESTION_LEN_MIN = 1
QUESTION_LEN_MAX = 1990
# 选项长度设定
OPTIONS_LEN_MIN = 4
OPTIONS_LEN_MAX = 990

# 本项目有5个模块，每个模块错误码分配1000个。0-999通用状态码；1000-1999为模块一使用，以此类推
ERROR_CODE = {
    "0": "ok",

    # questioner模块
    "1001": "入参失败",
    "1002": "用户名长度小于{}个字符".format(USER_NAME_LEN_MIN),
    "1003": "用户名长度大于{}个字符".format(USER_NAME_LEN_MAX),
    "1004": "密码长度小于{}".format(PWD_LEN_MIN),
    "1005": "密码长度大于{}".format(PWD_LEN_MAX),
    "1006": "该用户名已存在",
    "1007": "该登录用户名不存在",
    "1008": "该登密码错误",

    # questionnaire模块
    "2001": "入参失败",
    "2002": "问卷名长度小于{}个字符".format(QUESTIONNAIRE_NAME_LEN_MIN),
    "2003": "问卷名长度大于{}个字符".format(QUESTIONNAIRE_NAME_LEN_MAX),
    "2004": "操作用户不存在",
    "2005": "该问卷名已存在",
    "2006": "该问卷id不存在",

    # question模块
    "3001": "入参失败",
    "3002": "提交的问卷id不存在",
    "3003": "问题类型错误；不存在的问题类型",
    "3004": "问题长度小于{}个字符".format(QUESTION_LEN_MIN),
    "3005": "问题长度大于{}个字符".format(QUESTION_LEN_MAX),
    "3006": "选项长度小于{}个字符".format(OPTIONS_LEN_MIN),
    "3007": "选项长度大于{}个字符".format(OPTIONS_LEN_MAX),
    "3008": "提交的选项（options）计数后与选项个数（options_count）不同",

    # respondents模块
    "4001": "入参失败",
    "4002": "提交的问卷id不存在",
}
