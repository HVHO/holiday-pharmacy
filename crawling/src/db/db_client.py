from datetime import datetime

import pymysql
import os


class DbClient:
    insert_query_with_additional_info = 'INSERT INTO pharmacies (date, name, addr, open_time, close_time, addtional_info) VALUES (%s, %s, %s, %s, %s, %s)'
    insert_query_without_additional_info = 'INSERT INTO pharmacies (date, name, addr, open_time, close_time) VALUES (%s, %s, %s, %s, %s)'

    # constructor
    def __init__(self, host, db_name, username, password):
        # insert to db
        self.db_connector = pymysql.connect(host=host,
                                            user=username,
                                            password=password,
                                            db=db_name,
                                            charset='utf8')

        self.db_cursor = self.db_connector.cursor()


    # insert
    def insert(self, columns):
        for column in columns:
            if check_col_with_additional_info(column):
                self.insert_with_additional_info(column)
            else:
                self.insert_without_additional_info(column)

    # column : [ name, addr, phone num, start_time, end_time, type, additional_info ]
    def insert_with_additional_info(self, column):
        date = datetime.today().strftime('%Y-%m-%d')
        name = column[0]
        addr = column[1]
        phone_num = column[2]
        start_time = column[3]
        end_time = column[4]
        pharmacy_type = column[5]
        additional_info = column[6]

        self.db_cursor.execute(self.insert_query_with_additional_info,
                               (date, name, addr, start_time, end_time, additional_info))

    # column : [ name, addr, phone num, start_time, end_time, type]
    def insert_without_additional_info(self, column):
        date = datetime.today().strftime('%Y-%m-%d')
        name = column[0]
        addr = column[1]
        phone_num = column[2]
        start_time = column[3]
        end_time = column[4]
        pharmacy_type = column[5]

        self.db_cursor.execute(self.insert_query_without_additional_info, (date, name, addr, start_time, end_time))

    def commit(self):
        self.db_connector.commit()

    def finish(self):
        self.db_connector.commit()
        self.db_connector.close()


def check_col_with_additional_info(column):
    if len(column) > 7:
        return True
    else:
        return False
