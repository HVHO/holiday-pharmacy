from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from time import sleep


class Parser:
    # constructor
    def __init__(self, is_head_less = False):
        # chrome headless mode
        if is_head_less:
            options = webdriver.ChromeOptions()
            options.add_argument('headless')
            options.add_argument('window-size=1920x1080')
            options.add_argument("disable-gpu")
            self.driver = webdriver.Chrome("/Users/HVHO/Downloads/chromedriver", chrome_options=options)
        else:
            self.driver = webdriver.Chrome("/Users/HVHO/Downloads/chromedriver")


    def parse(self, year, month, day):
        # wait until driver load
        self.driver.implicitly_wait(3)
        self.driver.get('https://www.pharm114.or.kr/')

        # get into search menu
        menus = self.driver.find_elements_by_xpath("//ul[@id = 'menubar']//li[not(@class)]")
        menus[0].click()

        # fill the query

        Select(self.driver.find_element(By.NAME, "m_year")).select_by_visible_text(year)
        Select(self.driver.find_element(By.NAME, "m_month")).select_by_visible_text(month)
        Select(self.driver.find_element(By.NAME, "m_day")).select_by_visible_text(day)

        s_time = self.driver.find_element(By.NAME, "time_s1")

        Select(s_time).select_by_visible_text("전체")

        pharmacies = []

        addr1_pull_down_menu = self.driver.find_element(By.ID, "search2").find_element(By.NAME,"addr1")
        addr1_list = list(filter(lambda x: x != '', [x.get_attribute("value") for x in addr1_pull_down_menu.find_elements_by_tag_name("option")]))

        # output = open("/Users/HVHO/workspace/study/crawling/data.txt", 'w')
        result = []
        for addr1 in addr1_list:
            addr1_pull_down_menu = self.driver.find_element(By.ID, "search2").find_element(By.NAME, "addr1")
            Select(addr1_pull_down_menu).select_by_value(addr1)
            addr2_pull_down_menu = self.driver.find_element(By.ID, "search2").find_element(By.NAME,"addr2")
            addr2_list = list(filter(lambda x: x != '', [x.get_attribute("value") for x in addr2_pull_down_menu.find_elements_by_tag_name("option")]))

            for addr2 in addr2_list:
                addr1_pull_down_menu = self.driver.find_element(By.ID, "search2").find_element(By.NAME, "addr1")
                addr2_pull_down_menu = self.driver.find_element(By.ID, "search2").find_element(By.NAME, "addr2")

                Select(addr1_pull_down_menu).select_by_visible_text(addr1)
                Select(addr2_pull_down_menu).select_by_visible_text(addr2)
                button = self.driver.find_element(By.XPATH, "//input[@src='/images/sub1/search_butt.gif']")
                button.click()

                self.driver.switch_to.alert.accept()
                self.driver.implicitly_wait(2)

                print('searching,,, ' + addr1 + ' ' + addr2)
                try:
                    table = self.driver.find_element(By.XPATH, "//table[@style='TABLE-LAYOUT: fixed']")
                except:
                    print("there is no holiday pharmacy")
                    self.driver.back()
                    continue

                table_soup = BeautifulSoup(table.get_attribute('innerHTML'), 'html.parser')
                tbody_soup = table_soup.select('tbody')
                print(tbody_soup)
                # output.write(str(tbody_soup))
                result.append(str(tbody_soup))
                self.driver.back()
        sleep(3)

    def finish(self):
        self.driver.quit()