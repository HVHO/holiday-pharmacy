from datetime import datetime

import pymysql
import os


class DbClient:
    insert_query_with_additional_info = 'INSERT INTO pharmacies (date, name, addr, open_time, close_time, latitude, longitude, additional_info) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'
    insert_query_without_additional_info = 'INSERT INTO pharmacies (date, name, addr, open_time, close_time, latitude, longitude) VALUES (%s, %s, %s, %s, %s, %s, %s)'

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
            print("insert column: " + " ".join(column))
            if check_col_with_additional_info(column):
                self.insert_with_additional_info(column)
            else:
                self.insert_without_additional_info(column)

    # column : [ name, addr, phone num, start_time, end_time, type, additional_info, latitude, longitude]
    def insert_with_additional_info(self, column):
        date = datetime.today().strftime('%Y-%m-%d')
        name = column[0]
        addr = column[1]
        phone_num = column[2]
        start_time = column[3]
        end_time = column[4]
        pharmacy_type = column[5]
        additional_info = column[6]
        latitude = column[7]
        longitude = column[8]

        self.db_cursor.execute(self.insert_query_with_additional_info,
                               (date, name, addr, start_time, end_time, latitude, longitude, additional_info))

    # column : [ name, addr, phone num, start_time, end_time, type, latitude, longitude]
    def insert_without_additional_info(self, column):
        date = datetime.today().strftime('%Y-%m-%d')
        name = column[0]
        addr = column[1]
        phone_num = column[2]
        start_time = column[3]
        end_time = column[4]
        pharmacy_type = column[5]
        latitude = column[6]
        longitude = column[7]

        self.db_cursor.execute(self.insert_query_without_additional_info, (date, name, addr, start_time, end_time, latitude, longitude))

    def commit(self):
        self.db_connector.commit()

    def finish(self):
        self.db_connector.commit()
        self.db_connector.close()


def check_col_with_additional_info(column):
    if len(column) > 8:
        return True
    else:
        return False
