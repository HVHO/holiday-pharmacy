from datetime import time

from crawling.src.parser.parser import Parser

# options
CHROME_HEAD_LESS_MODE = True


def main():
    parser = Parser(CHROME_HEAD_LESS_MODE)
    parser.parse('2020', '12', "2")


main()
