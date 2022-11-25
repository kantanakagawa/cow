import chromedriver_binary
from selenium import webdriver
from time import sleep
import openpyxl
import pandas as pd
driver = webdriver.Chrome()
driver.get('https://www.kenchikukyo.jp/schedule/')

class Sucreiping:
    
    def get_year(self):
        l = []
        next_link = driver.find_elements_by_class_name("schedule-archive__item")
        for i in next_link:
            atag = i.find_element_by_tag_name("a")
            l.append(atag.get_attribute("href"))
        return l
    def cow_scraping(self, url):
        driver.get(url)
        cow_list = []
        for elem_span in driver.find_elements_by_xpath("//a/span"):
            sleep(1)
            elem_a = elem_span.find_element_by_xpath("..")
            if elem_span.text == "和牛子牛黒毛和種":
                cow_list.append(elem_a.get_attribute("href"))
        url_list = []
        for cow_link in cow_list:
            sleep(1)
            driver.get(cow_link)
            element_class = driver.find_elements_by_class_name("single-schedule__data")
            for i in element_class:
                atag = i.find_element_by_tag_name("a")
                url_list.append(atag.get_attribute("href"))
        return url_list[3::4]
    def cow_scraping_2020(self, url):
        driver.get(url)
        cow_list = []
        for elem_span in driver.find_elements_by_xpath('//a/span'):
            sleep(1)
            elem_a = elem_span.find_element_by_xpath('..')
            if elem_span.text == "和牛子牛黒毛和種" :
                cow_list.append(elem_a.get_attribute('href'))
        cow_list = cow_list[4:]
        url_list = []
        for cow_link in cow_list:
            sleep(1)
            driver.get(cow_link)
            element_class = driver.find_elements_by_class_name("single-schedule__data")
            for i in element_class:
                atag = i.find_element_by_tag_name("a")
                url_list.append(atag.get_attribute("href"))
        return url_list[3::4]
    def extract(self, filepath):
        _df=pd.read_excel(filepath)
        columns=_df.iloc[1,[2,3,4,5,6,7,8,9]]
        df=_df.iloc[2:len(_df),[2,3,4,5,6,7,8,9]]
        df.columns=columns
        dating = _df.columns[1]
        d = dating.find("\u3000")
        dd = _df.columns[1][:d]
        df = df.assign(年月日=dd)
        return df
    def get_data(self):
        l = self.get_year()
        l_0 = l[0]
        l_1 = l[1]
        l_2 = l[2]
        xlsx_list_2022 = self.cow_scraping(l_0)
        xlsx_list_2021 = self.cow_scraping(l_1)
        xlsx_list_2020 = self.cow_scraping_2020(l_2)
        all_xlsx_list = xlsx_list_2022+xlsx_list_2021+xlsx_list_2020
        df=pd.DataFrame()
        for filepath in all_xlsx_list:
            _df=self.extract(filepath)
            df=pd.concat([df,_df])
        df.dropna()
        df=df.reset_index(drop=True)
        driver.close()
        return df