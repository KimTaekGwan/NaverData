from dotenv import load_dotenv
import os
import random

from bs4 import BeautifulSoup
import requests
import pandas as pd


import time
from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


class DataProduct:
    def __init__(self) -> None:
        self._setting()

    def _setting(self):
        load_dotenv()
        self.client_id = os.getenv("client_id")
        self.client_secret = os.getenv("client_secret")
        options = Options()
        options.add_experimental_option('detach', True)
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        service = Service(ChromeDriverManager().install())

    def getdata_naverapi(self, url, params):
        headers = {'X-Naver-Client-Id': self.client_id,
                   'X-Naver-Client-Secret': self.client_secret}

        r = requests.get(url, params=params, headers=headers)
        rescode = r.status_code

        if rescode == 200:
            res = r.json()
            return res
        else:
            print(f"Error Code: {rescode} | query: {params['query']}")

    def _set_params(self, keyword):
        total_params = []
        # for s, d in [[1, 99], [100, 100]]:
        for s, d in [[1, 100]]:
            params = {'query': keyword,
                      'display': d,
                      'start': s,
                      'sort': 'sim'}  # 파라미터
            total_params.append(params)
        return total_params

    def extract_product_info(self, keyword):
        url = 'https://openapi.naver.com/v1/search/shop.json'  # api 주소

        total_params = self._set_params(keyword=keyword)
        res = []
        for params in total_params:
            result = self.getdata_naverapi(url, params)
            if result:
                for item in result['items']:
                    name = item['title']
                    lprice = item['lprice']
                    hprice = item['hprice']
                    link = item['link']
                    mallName = item['mallName']
                    maker = item['maker']
                    brand = item['brand']
                    category1 = item['category1']
                    category2 = item['category2']
                    category3 = item['category3']
                    category4 = item['category4']
                    product_naver_id = item['productId']

                    soup = BeautifulSoup(name, 'html.parser')
                    cl_name = soup.get_text()
                    dic = {
                        'name': cl_name,
                        'lprice': lprice,
                        'hprice': hprice,
                        'link': link,
                        'mallName': mallName,
                        'maker': maker,
                        'brand': brand,
                        'category1': category1,
                        'category2': category2,
                        'category3': category3,
                        'category4': category4,
                        'product_naver_id': product_naver_id
                    }

                    res.append(dic)

        return res

    def run(self):
        pass


if __name__ == '__main__':
    load_csv_path = 'last/data/Keywords_Top.csv'
    save_csv_path = 'last/data/Data_Product.csv'
    search_id = 1

    df = pd.read_csv(load_csv_path)
    df_id = df[df['search_id'] == search_id]

    # top : 100
    keywords = df_id['keyword'].to_list()[:100]

    total = []
    dataproduct = DataProduct()
    for keyword in tqdm(keywords):
        total += dataproduct.extract_product_info(keyword)

    df = pd.DataFrame(total)
    # print(df.head(4))
    # df.columns = ['ranking','keyword']
    df['search_id'] = 1
    df['crawling'] = 0
    df.to_csv(save_csv_path, index=False, sep='\t')
