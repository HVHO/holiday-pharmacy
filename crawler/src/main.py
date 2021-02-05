import os
import time
from datetime import datetime
from crawler.config.config import load_config
from crawler.src.db.db_client import DbClient
from crawler.src.map_client.kakao_map_client import KakaoMapClient
from crawler.src.parser.parser import Parser

# options
CHROME_HEAD_LESS_MODE = True


def main():
    # load config
    config = load_config()

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


    search_start_time = datetime.now()
    print("======================Map api request start==========================")
    print("=====================================================================")

    map_client = KakaoMapClient(config["kakao_auth_key"])
    searched_pharmacies = map_client.get_latitude_and_longitudes(pharmacies)

    print("======================Map api request End============================")
    print("|  whole parsed pharmacy num: " + str(len(searched_pharmacies)))
    print("|  time taken: ", str(datetime.now() - search_start_time).split(".")[0])
    print("=====================================================================")

    # load db config

    db_start_time = datetime.now()

    print("==========================DB insert Start============================")
    print("| db host: " + config["host"])
    print("| db user: " + config["user"])
    print("| db table: " + config["name"])
    print("=====================================================================")

    # insert to db
    db_client = DbClient(config["host"], config["name"], config["user"], config["pass"])
    db_client.insert(searched_pharmacies)
    db_client.finish()

    print("==========================DB insert End==============================")
    print("|  time taken: ", str(datetime.now() - db_start_time).split(".")[0])
    print("=====================================================================")



main()
