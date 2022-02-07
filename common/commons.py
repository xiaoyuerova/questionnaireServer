import json
import os
import datetime
from datetime import timedelta
from conf.base import SPE_CH


def http_response(self, msg, code):
    """
    response:
            "data":{type1:{},type2:{}}  对象转成的字典,以type为key区分并访问每一行
            "code":code
    """
    self.write(json.dumps({"data": {"msg": msg, "code": code}}))


def save_files(file_metas, in_rel_path, type='image'):
    """
    Save file stream to server
    :param file_metas:
    :param in_rel_path:
    :param type:
    :return:
    """
    file_path = ""
    file_name_list = []
    for meta in file_metas:
        file_name = meta['filename']
        file_path = os.path.join(in_rel_path, file_name)
        file_name_list.append(file_name)
        # save image as binary
        with open(file_path, 'wb') as up:
            up.write(meta['body'])
    return file_name_list


def list_to_dict(object_list):
    """
    将数据库存储格式的对象列表转换为字典列表
    :param object_list: 对象列表（数据行列表）
    :return: 字典列表
    """
    dict_list = []
    for item in object_list:
        dict_ = item.__dict__
        del dict_['_sa_instance_state']
        dict_list.append(json.dumps(dict_))
    return dict_list


def get_dates(start_date, end_date):
    """
    获取时间段内每一天的日期
    :param start_date: 开始日期，字符串格式
    :param end_date: 终止日期，字符串格式
    :return: 时间段内每一天的日期列表
    """
    date_list = []
    start = datetime.datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.datetime.strptime(end_date, "%Y-%m-%d")
    while start <= end:
        date_str = start.strftime("%Y-%m-%d")
        date_list.append(date_str)
        start += timedelta(days=1)
    return date_list


def option_union(options):
    """
    选项联合;
    例：[’12‘，’8‘，’10‘，’5‘] => ’12&8&10&5&‘
    :param options: list;选项列表;
    :return: 选项列表
    """
    options_union = ''
    for option in options:
        if type(option) != str:
            option = str(option)
        options_union = options_union + option + SPE_CH
    return options_union


def option_parsing(options_union):
    """
    选项解析;
    例：’12&8&10&5&‘ => [’12‘，’8‘，’10‘，’5‘]
    :param options_union: str;以特殊字符结尾联合好的选项;
    :return: 选项列表
    """
    options = []
    option = ''
    for ch in options_union:
        if ch == SPE_CH:
            options.append(option)
            option = ''
        else:
            option = option + ch
    return options


if __name__ == "__main__":
    http_response()