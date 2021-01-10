import time
import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from time import sleep
import re


class Parser:
    # constructor
    def __init__(self, is_head_less=False):
        # chrome headless mode
        if is_head_less:
            options = webdriver.ChromeOptions()
            options.add_argument('headless')
            options.add_argument('window-size=1920x1080')
            options.add_argument("disable-gpu")
            # todo : replace chromedriver location by environment variable
            self.driver = webdriver.Chrome("/Users/HVHO/Downloads/chromedriver", chrome_options=options)
        else:
            self.driver = webdriver.Chrome("/Users/HVHO/Downloads/chromedriver")

    def parse(self, year, month, day):

        # wait until driver load
        self.driver.implicitly_wait(3)
        self.driver.get('https://www.pharm114.or.kr/')
        try:
            self.driver.switch_to.alert.accept()
        except:
            print("accept alert")
        # get into search menu
        self.go_to_search_menu()

        pharmacies = []

        addr1_pull_down_menu = self.driver.find_element(By.ID, "search2").find_element(By.NAME, "addr1")
        addr1_list = list(filter(lambda x: x != '', [x.get_attribute("value") for x in
                                                     addr1_pull_down_menu.find_elements_by_tag_name("option")]))

        # output = open("/Users/HVHO/workspace/study/crawler/data.txt", 'w')
        result = []
        for addr1 in addr1_list:
            addr1_pull_down_menu = self.driver.find_element(By.ID, "search2").find_element(By.NAME, "addr1")
            Select(addr1_pull_down_menu).select_by_value(addr1)
            addr2_pull_down_menu = self.driver.find_element(By.ID, "search2").find_element(By.NAME, "addr2")
            addr2_list = list(filter(lambda x: x != '', [x.get_attribute("value") for x in
                                                         addr2_pull_down_menu.find_elements_by_tag_name("option")]))

            for addr2 in addr2_list:

                # fill the date query
                self.fill_date_query(year, month, day)
                # fill address query
                self.fill_addr_query(addr1, addr2)
                # press search button
                button = self.driver.find_element(By.XPATH, "//input[@src='/images/sub1/search_butt.gif']")
                button.click()
                # accept alert
                self.driver.switch_to.alert.accept()
                # self.driver.implicitly_wait(2)

                print('Searching,,, ' + addr1 + ' ' + addr2)

                try:
                    self.driver.find_element(By.XPATH, "//table[@style='TABLE-LAYOUT: fixed']")
                except:
                    print("There is no holiday pharmacy")
                    self.go_to_search_menu()
                    continue

                # get search pages number
                page_anchors = self.driver.find_element(By.XPATH, "//td[@style='padding : 2 0 0 0']").find_elements(
                    By.TAG_NAME, 'a')

                for page_idx in range(len(page_anchors) + 1):

                    table = self.driver.find_element(By.XPATH, "//table[@style='TABLE-LAYOUT: fixed']")
                    table_soup = BeautifulSoup(table.get_attribute('outerHTML'), 'html.parser').find('table', attrs={
                        'style': 'TABLE-LAYOUT: fixed'})

                    prev_pharamacy = ["", "", "", "", "", "",
                                      ""]  # name, addr, phone num, type, start_time, end_time, additional info
                    for idx, tr in enumerate(table_soup.find_all('tr')):
                        if tr.has_attr("style") and tr["style"] == "display:none":
                            continue

                        td_array = tr.find_all('td')

                        if len(td_array) == 7:
                            if prev_pharamacy[0] != "":
                                pharmacies.append(prev_pharamacy)
                                print(prev_pharamacy)
                            prev_pharamacy = self.main_row_parser(tr)
                        elif "위치정보" in td_array[0].get_text():
                            prev_pharamacy.append(self.sub_row_parser(tr))
                    pharmacies.append(prev_pharamacy)

                    if page_idx < len(page_anchors):
                        self.driver.find_element(By.XPATH, "//td[@style='padding : 2 0 0 0']").find_elements(
                            By.TAG_NAME, 'a')[page_idx].click()

                # back to search menu
                self.go_to_search_menu()

        sleep(3)
        return pharmacies

    ## parse main row
    def main_row_parser(self, table_row):
        td_array = table_row.find_all('td')
        regex = re.compile(r'[\n\r\t]')
        # parse pharmacy name
        name = regex.sub('', td_array[1].get_text())
        # parse pharmacy address
        addr = regex.sub('', td_array[2].get_text()).replace(u'\xa0', u' ')
        # parse pharmacy phone number
        phone_num = regex.sub('', td_array[3].get_text())
        # parse pharmacy available time
        available_time = regex.sub('', td_array[4].get_text())
        (start_time, end_time) = available_time.split('~')
        start_time = start_time.strip()
        end_time = end_time.strip()
        if "익일" in end_time:
            hour = format(int(list(end_time)[2]) * 10 + int(list(end_time)[3]) + 24, '02d')
            minute = format(int(list(end_time)[5]) * 10 + int(list(end_time)[6]), '02d')
            end_time = str(hour) + ":" + str(minute)
        # parse pharmacy type
        parm_type = regex.sub('', td_array[5].get_text())

        return [name, addr, phone_num, start_time, end_time, parm_type]

    # parse sub row
    def sub_row_parser(self, table_row):
        td_array = table_row.find_all('td')
        regex = re.compile(r'[\n\r\t]')
        additional_info = regex.sub('', td_array[0].get_text())
        additional_info = additional_info.replace("위치정보", "")
        additional_info = additional_info.replace("[", "")
        additional_info = additional_info.replace("]", "")
        additional_info = additional_info.replace(":", "")
        additional_info = ' '.join(additional_info.split())
        return additional_info

    def go_to_search_menu(self):
        menus = self.driver.find_elements_by_xpath("//ul[@id = 'menubar']//li[not(@class)]")
        menus[0].click()

    def fill_date_query(self, year, month, day):
        Select(self.driver.find_element(By.NAME, "m_year")).select_by_visible_text(year)
        Select(self.driver.find_element(By.NAME, "m_month")).select_by_visible_text(month)
        Select(self.driver.find_element(By.NAME, "m_day")).select_by_visible_text(day)
        s_time = self.driver.find_element(By.NAME, "time_s1")
        Select(s_time).select_by_visible_text("전체")

    def fill_addr_query(self, addr1, addr2):
        addr1_pull_down_menu = self.driver.find_element(By.ID, "search2").find_element(By.NAME, "addr1")
        addr2_pull_down_menu = self.driver.find_element(By.ID, "search2").find_element(By.NAME, "addr2")
        Select(addr1_pull_down_menu).select_by_visible_text(addr1)
        Select(addr2_pull_down_menu).select_by_visible_text(addr2)

    def finish(self):
        self.driver.quit()
