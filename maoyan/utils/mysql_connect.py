# -*- coding: utf-8 -*-
__author__ = 'lateink'
import MySQLdb
import MySQLdb.cursors
from maoyan.settings import MYSQL_HOST, MYSQL_DBNAME, MYSQL_USER, MYSQL_PASSWORD


class Mysqlconnect(object):
    db = MySQLdb.connect(MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DBNAME, charset="utf8")
    cursor = db.cursor()

    def get(self):
        """
        返回的是generator
        :return:
        """
        self.cursor.execute('SELECT name FROM amazon_book')
        results = self.cursor.fetchall()
        names = (result[0] for result in results)
        return names

    def close(self):
        self.db.close()


if __name__ == '__main__':
    db_connect = Mysqlconnect()
    names = db_connect.get()
    db_connect.close()
    print(type(names))
    print(next(names))

