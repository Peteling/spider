# -*- coding: utf-8 -*-
__author__ = 'lateink'
import datetime
import re


def date_format(date_string):
    date = ""
    try:
        date = datetime.datetime.strptime(date_string, "%d %b, %Y").date()
    except:
        year = date_string[-4:]
        if year.isdigit() and len(date_string) > 4:
            date = datetime.datetime.strptime(date_string, "%B %Y").date()
        elif year.isdigit() and len(date_string) == 4:
            date = datetime.datetime.strptime(date_string, "%Y").date()
        else:
            return date_string
    return date


def get_player(example, flag=1):
    if example == "无用户评测":
        return 0
    l = re.findall('\d+', example)
    if len(l) == 0:
        return 0
    elif len(l) > 1 and flag == 0:
        return l[0] + '%'
    elif flag == 1:
        return l[1]


def system_format(system_item):
    if len(system_item) == 0:
        system_item.append("Windows")
        return system_item
    else:
        if len(system_item[-1]) == 0:
            system_item.remove(system_item[-1])
            return system_item


if __name__ == '__main__':
    # date = date_format("16 Sep, 2016")
    # print(type(date))
    # print(date)
    get_player("68% of the 251 user reviews in the last 30 days are")