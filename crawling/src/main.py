from datetime import time

import request
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from time import sleep


def main():
    driver = webdriver.Chrome("/Users/HVHO/Downloads/chromedriver")
    # wait until driver load
    driver.implicitly_wait(3)
    driver.get('https://www.pharm114.or.kr/')

    # get into search menu
    menus = driver.find_elements_by_xpath("//ul[@id = 'menubar']//li[not(@class)]")
    menus[0].click()

    # fill the query
    year = driver.find_element(By.NAME, "m_year")
    month = driver.find_element(By.NAME, "m_month")
    day = driver.find_element(By.NAME, "m_day")

    Select(year).select_by_visible_text("2020")
    Select(month).select_by_visible_text("1")
    Select(day).select_by_visible_text("1")

    s_time = driver.find_element(By.NAME, "time_s1")

    Select(s_time).select_by_visible_text("전체")

    pharmacies = []

    addr1_pull_down_menu = driver.find_element(By.ID, "search2").find_element(By.NAME,"addr1")
    addr1_list = list(filter(lambda x: x != '', [x.get_attribute("value") for x in addr1_pull_down_menu.find_elements_by_tag_name("option")]))

    output = open("/Users/HVHO/workspace/study/crawling/data.txt", 'w')
    for addr1 in addr1_list:
        addr1_pull_down_menu = driver.find_element(By.ID, "search2").find_element(By.NAME, "addr1")
        Select(addr1_pull_down_menu).select_by_value(addr1)
        addr2_pull_down_menu = driver.find_element(By.ID, "search2").find_element(By.NAME,"addr2")
        addr2_list = list(filter(lambda x: x != '', [x.get_attribute("value") for x in addr2_pull_down_menu.find_elements_by_tag_name("option")]))

        for addr2 in addr2_list:
            addr1_pull_down_menu = driver.find_element(By.ID, "search2").find_element(By.NAME, "addr1")
            addr2_pull_down_menu = driver.find_element(By.ID, "search2").find_element(By.NAME, "addr2")

            Select(addr1_pull_down_menu).select_by_visible_text(addr1)
            Select(addr2_pull_down_menu).select_by_visible_text(addr2)
            button = driver.find_element(By.XPATH, "//input[@src='/images/sub1/search_butt.gif']")
            button.click()

            driver.switch_to.alert.accept()
            driver.implicitly_wait(2)

            print('searching,,, ' + addr1 + ' ' + addr2)
            try:
                table = driver.find_element(By.XPATH, "//table[@style='TABLE-LAYOUT: fixed']")
            except:
                print("there is no holiday pharmacy")
                driver.back()
                continue

            table_soup = BeautifulSoup(table.get_attribute('innerHTML'), 'html.parser')
            tbody_soup = table_soup.select('tbody')
            # print(tbody_soup)
            output.write(str(tbody_soup))
            driver.back()

    sleep(3)
    driver.quit()


main()
