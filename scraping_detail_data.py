import chromedriver_binary
from selenium import webdriver
from time import sleep
import openpyxl
import pandas as pd

driver = webdriver.Chrome()
driver.get('https://www.kenchikukyo.jp/schedule/')

class Sucraping_detail:

    def get_years(self):
        l = []
        next_link = driver.find_elements_by_class_name("schedule-archive__item")
        for i in next_link:
            atag = i.find_element_by_tag_name("a")
            l.append(atag.get_attribute("href"))
        return l

    def listing_scraping(self,url):
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
        return url_list

    def make_nkb_list(self,year_urls):
        url_list = []
        for i in year_urls:
            url = self.listing_scraping(i)
            url_list.append(url)

        nkb_url = []

        for url_lists in url_list:
            for i in url_lists:
                if 0 < i.find("NKB.xlsx"):
                    if 0>i.find("KDNKB.xlsx"):
                        nkb_url.append(i)

        bull_list = ['https://www.kenchikukyo.jp/wp-content/uploads/2020/09/R020910NKB.xlsx','https://www.kenchikukyo.jp/wp-content/uploads/2020/09/R020911NKB.xlsx','https://www.kenchikukyo.jp/wp-content/uploads/2020/08/R020807NKB.xlsx','https://www.kenchikukyo.jp/wp-content/uploads/2020/08/R020806NKB.xlsx','https://www.kenchikukyo.jp/wp-content/uploads/2020/07/R020710NKB.xlsx','https://www.kenchikukyo.jp/wp-content/uploads/2020/07/R020709NKB.xlsx','https://www.kenchikukyo.jp/wp-content/uploads/2020/06/R020612NKB.xlsx','https://www.kenchikukyo.jp/wp-content/uploads/2020/06/R020611NKB.xlsx','https://www.kenchikukyo.jp/wp-content/uploads/2020/05/R020515NKB.xlsx','https://www.kenchikukyo.jp/wp-content/uploads/2020/05/R020514NKB.xlsx',]

        for i in bull_list:
            index = nkb_url.index(i)
            nkb_url.pop(index)
        return nkb_url

    def extrac(self,file_path):
        _df=pd.read_excel(file_path)
        df = _df.iloc[3:,1:27]
        df.columns = _df.iloc[2,1:27]
        d = _df.iloc[0][1]
        aa = d.find("月")
        bb = d.find("月",aa+1)
        dd = d[:aa] + d[bb:-5]
        df = df.assign(年月日=dd)
        return df

    def get_detail_data(self):
        year_urls = self.get_years()
        nkb_list = self.make_nkb_list(year_urls)
        df=pd.DataFrame()
        for file_path in nkb_list:
            _df=self.extrac(file_path)
            df=pd.concat([df,_df])
        df=df.reset_index(drop=True)
        driver.close()
        return df