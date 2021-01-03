from datetime import time, datetime

from crawling.src.parser.parser import Parser

# options
CHROME_HEAD_LESS_MODE = True


def main():
    # parse today's holiday pharmacy
    query_year = str(datetime.today().year)
    query_month = str(datetime.today().month)
    query_day = str(datetime.today().day)

    print("=============================Query Start=============================")
    print("|  year : " + query_year + "                                                       |")
    print("|  month : " + query_month + "                                                        |")
    print("|  day : " + query_day + "                                                          |")
    print("=====================================================================")
    parser = Parser(CHROME_HEAD_LESS_MODE)

    pharmacies = parser.parse(query_year, query_month, query_day)





main()
