# -*- coding: utf-8 -*-
__author__ = 'lateink'


class transCookie(object):
    def __init__(self, cookie):
        self.cookie = cookie

    def stringToDict(self):
        itemDict = {}
        items = self.cookie.split(';')
        for item in items:
            key = item.split('=')[0].replace(' ', '')
            value = item.split('=')[1]
            itemDict[key] = value
        return itemDict


if __name__ == '__main__':
    cookie = 'mature_content=1; browserid=1192744352752170434; steamCountry=CN%7C3d9c67a70c7b41aadb69aab8f493f1e3; ' \
             'sessionid=e60a7cb19768626386f2cb11; ' \
             'app_impressions=20500@1_7_7_230_150_1|431960@1_7_7_230_150_1|271590@1_7_7_230_150_1|650760' \
             '@1_7_7_230_150_1|230410@1_7_7_230_150_1|275850@1_7_7_230_150_1|359550@1_7_7_230_150_1|433850' \
             '@1_7_7_230_150_1|730@1_7_7_230_150_1|578080@1_7_7_230_150_1|570@1_7_7_230_150_1|475150@1_7_7_230_150_1' \
             '|462780@1_7_7_230_150_1; recentapps=%7B%22578080%22%3A1502762163%2C%22570%22%3A1502523811%7D; ' \
             'timezoneOffset=28800,0; _ga=GA1.2.923130958.1502522632; _gid=GA1.2.1404227983.1502762179 '
    trans = transCookie(cookie)
    dict1 = trans.stringToDict()
    print(dict1)
