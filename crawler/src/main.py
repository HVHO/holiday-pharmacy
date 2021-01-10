import os
import time
from datetime import datetime
from crawler.config.config import config
from crawler.src.db.db_client import DbClient
from crawler.src.parser.parser import Parser

# options
CHROME_HEAD_LESS_MODE = True


def main():
    # parse today's holiday pharmacy
    query_year = str(datetime.today().year)
    query_month = str(datetime.today().month)
    query_day = str(datetime.today().day)
    query_start_time = datetime.now()

    print("==========================Query Start================================")
    print("|  year : " + query_year)
    print("|  month : " + query_month)
    print("|  day : " + query_day)
    print("=====================================================================")


    parser = Parser(CHROME_HEAD_LESS_MODE)
    pharmacies = parser.parse(query_year, query_month, query_day)

    print("==========================Query End==================================")
    print("|  whole parsed pharmacy num: " + str(len(pharmacies)))
    print("|  time taken: ", str(datetime.now() - query_start_time).split(".")[0])
    print("=====================================================================")

    # load db config
    db_config = config()
    db_start_time = datetime.now()

    print("==========================DB insert Start============================")
    print("| db host: " + db_config["host"])
    print("| db user: " + db_config["user"])
    print("| db table: " + db_config["name"])
    print("=====================================================================")

    # insert to db
    db_client = DbClient(db_config["host"], db_config["name"], db_config["user"], db_config["pass"])
    db_client.insert(pharmacies)
    db_client.finish()

    print("==========================DB insert End==============================")
    print("|  time taken: ", str(datetime.now() - db_start_time).split(".")[0])
    print("=====================================================================")



main()
