from dotenv import load_dotenv
import os
import random
import re
import numpy as np

from bs4 import BeautifulSoup
import requests
import pandas as pd


import time
from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By


class DataReviews:
    def __init__(self) -> None:
        self.review_list = []
        self._setting()

    def _setting(self):
        load_dotenv()
        self.client_id = os.getenv("client_id")
        self.client_secret = os.getenv("client_secret")

        self.options = Options()
        self.options.add_argument('headless')

        # options.add_argument("--start-maximized")  # add
        # options.add_argument("--window-size=1920,1080")  # add
        self.options.add_experimental_option('detach', True)
        self.options.add_experimental_option(
            'excludeSwitches', ['enable-logging'])

        self.service = Service(ChromeDriverManager().install())

    # 리뷰 데이터 추출
    def _score_extract(self, element):
        return int(re.findall(r'\d+', element.text)[0])

    def _idx_extract(self, infos):
        try:
            try:
                if infos.text[-1] == '*':
                    idx = True
                else:
                    idx = False
            except:
                idx = False
            return idx
        except:
            # print(infos.text)
            return 'error'

    def _text_extract(self, infos):
        res = infos.text
        res = res.replace("\n", " ")
        return res

    def _extract_review_data(self, reviews, product_id):
        # 평점
        scores = reviews.find_elements(
            By.CLASS_NAME, "reviewItems_average__0kLWX")
        scores = list(map(self._score_extract, scores))

        # 리뷰에서 스토어, ID, DATE 추출
        infos = reviews.find_elements(By.CLASS_NAME, "reviewItems_etc__9ej69")

        # print(infos)
        id_idxs = list(map(self._idx_extract, infos))
        infos = list(map(self._text_extract, infos))

        ids = []
        dates = []
        product_ids = []

        for id, b in enumerate(id_idxs):
            if b == True:
                ids.append(infos[id])
                dates.append(infos[id+1])
                product_ids.append(product_id)

        # 리뷰에서 데이터 추출
        datas = reviews.find_elements(By.CLASS_NAME, "reviewItems_text__XrSSf")
        datas = list(map(self._text_extract, datas))
        return list(zip(product_ids, ids, scores, dates, datas))

    # 활성 페이지 찾기
    def _search_index(self, a_list):
        for idx, a in enumerate(a_list):
            try:
                now = [True, a.find_element(By.TAG_NAME, 'span')]
                return idx
            except:
                now = [False, []]

    # 네이버 쇼핑
    def crawling_reviews(self, name, product_id, link):
        print(name)
        try:
            driver = webdriver.Chrome(
                service=self.service, options=self.options)
            driver.get(link)
            time.sleep(random.uniform(1, 2))
            # try:
            xpath = '//*[@id="wrap"]/div[2]/a[2]'
            element = driver.find_element(By.XPATH, xpath)
            element.click()

            start_time = time.time()  # 시작
            while True:
                # 리뷰 엘리먼트 탐색
                time.sleep(random.uniform(1, 1.5))
                xpath = '//*[@id="section_review"]/ul'
                reviews = driver.find_element(By.XPATH, xpath)

                self.review_list += self._extract_review_data(
                    reviews, str(int(product_id)))

                # 페이지 넘기기
                xpath = '//*[@id="section_review"]/div[3]'
                page_views = driver.find_element(By.XPATH, xpath)
                a_list = page_views.find_elements(By.TAG_NAME, 'a')

                idx = self._search_index(a_list)
                page_num = a_list[idx].text.split('\n')[1]
                # print('Page', page_num)
                if int(page_num) == 100:
                    break
                if (len(a_list)-1) != idx:
                    # print(a_list[idx].text.split('\n')[1])
                    a_list[idx+1].click()
                else:
                    # print('end')
                    break
            print(f"걸린시간: {time.time() - start_time}")
            driver.close()
            return True
        except:
            driver.close()
            return False

    def run(self):
        pass


if __name__ == '__main__':
    load_csv_path = 'last/data/Data_Product.csv'
    save_csv_path = 'last/data/Data_Reviews.csv'
    search_id = 1

    datareviews = DataReviews()
    df_product = pd.read_csv(load_csv_path, sep='\t')

    print(len(df_product))
    df_product.drop_duplicates('product_naver_id', inplace=True)
    print(len(df_product))
    for idx, crawling in enumerate(df_product['crawling']):
        if crawling == 0:
            chk = datareviews.crawling_reviews(
                df_product['name'][idx],
                df_product['product_naver_id'][idx],
                df_product['link'][idx])
            if chk == False:
                df_product['crawling'][idx] = 1
            else:
                df_product['crawling'][idx] = 2
                df = pd.DataFrame(datareviews.review_list)
                df.columns = ['product_naver_id',
                              'id', 'score', 'date', 'data']
                df['search_id'] = 1
                reviews_df = pd.read_csv(save_csv_path, sep='\t')
                combined_df = pd.concat([reviews_df, df], axis=0)
                combined_df.to_csv(save_csv_path, index=False, sep='\t')
                df_product.to_csv(load_csv_path, index=False, sep='\t')

    # df_product.apply(lambda row: datareviews.crawling_reviews(
    #     row['name'], row['product_id'], row['link']), axis=1)
    # df = pd.DataFrame(datareviews.review_list)
    # df.columns = ['product_id', 'id', 'score', 'date', 'data']
    # df['search_id'] = 1
    # df.to_csv(save_csv_path, index=False, sep='\t')
