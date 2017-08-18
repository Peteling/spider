# -*- coding: utf-8 -*-
__author__ = 'lateink'
import hashlib
import re
import datetime


def get_md5(url):
    if isinstance(url, str):
        url = url.encode('utf-8')
    m = hashlib.md5()
    m.update(url)
    return m.hexdigest()


def split_blank(value_list):
    print(value_list)
    value_list = [value.replace(" ", "") for value in value_list]
    value_list = [value.replace("\n", "") for value in value_list]
    print(value_list)
    sep = ","
    value = sep.join(value_list)
    print(value)
    return value


def date_converts(value):
    value = value.replace('\n', '')
    value = value.replace(' ', '')
    regex_str = ".*?(\d+(-\d*-\d*)*).*"
    match_obj = re.match(regex_str, value)
    if match_obj:
        value = match_obj.group(1)
    else:
        value = ""
    return value


def get_place(value):
    regex = re.compile('[\u4e00-\u9fa5]+')
    value = regex.findall(value)
    if len(value) != 0:
        return value[0]
    else:
        return ""


def return_value(value):
    return value


def get_film_id(url):
    regex_str = ".*?(\d+)"
    match_obj = re.match(regex_str, url)
    value = ""
    if match_obj:
        value = match_obj.group(1)
    return value

if __name__ == '__main__':
    # print(date_converts("\n   \n  2017-10-14 \n中国大陆\n   sdf\n"))
    # print(get_place("\n  2017  中国大陆  \n"))
    split_blank(['\n  lateink\n', '\n bojack\n', 'lexburner'])
