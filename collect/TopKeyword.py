import time
import random

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


class TopKeyword:
    def __init__(self) -> None:
        self.options = None
        self.service = None
        self.driver = None
        self.xpath_dict = {}
        self.setting()
        self.xpath_set()

    def setting(self):
        self.options = Options()
        self.options.add_experimental_option('detach', True)
        self.options.add_experimental_option(
            'excludeSwitches', ['enable-logging'])
        self.service = Service(ChromeDriverManager().install())

    def xpath_set(self):
        self.xpath_dict['category_1'] = '//*[@id="content"]/div[2]/div/div[1]/div/div/div[1]/div/div[1]/span'
        self.xpath_dict['category_1_value'] = '//*[@id="content"]/div[2]/div/div[1]/div/div/div[1]/div/div[1]/ul/li[6]/a'
        self.xpath_dict['category_2'] = '//*[@id="content"]/div[2]/div/div[1]/div/div/div[1]/div/div[2]/span'
        self.xpath_dict['category_2_value'] = '//*[@id="content"]/div[2]/div/div[1]/div/div/div[1]/div/div[2]/ul/li[5]/a'
        self.xpath_dict['category_3'] = '//*[@id="content"]/div[2]/div/div[1]/div/div/div[1]/div/div[3]/span'
        self.xpath_dict['category_3_value'] = '//*[@id="content"]/div[2]/div/div[1]/div/div/div[1]/div/div[3]/ul/li[4]/a'
        self.xpath_dict['period'] = '//*[@id="content"]/div[2]/div/div[1]/div/div/div[2]/div[1]/span/label[3]'
        self.xpath_dict['device'] = '//*[@id="content"]/div[2]/div/div[1]/div/div/div[3]/div/div/span[1]'
        self.xpath_dict['gender'] = '//*[@id="content"]/div[2]/div/div[1]/div/div/div[4]/div/div/span[2]'
        self.xpath_dict['age'] = ['//*[@id="content"]/div[2]/div/div[1]/div/div/div[5]/div/div/span[4]',
                                  '//*[@id="content"]/div[2]/div/div[1]/div/div/div[5]/div/div/span[5]']
        self.xpath_dict['search'] = '//*[@id="content"]/div[2]/div/div[1]/div/a'
        self.xpath_dict['top20'] = '//*[@id="content"]/div[2]/div/div[2]/div[2]/div/div/div[1]/ul'
        self.xpath_dict['next'] = '//*[@id="content"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/a[2]'

    def _click(self, xpath):
        element = self.driver.find_element(By.XPATH, xpath)
        element.click()

    def run(self):
        self.driver = webdriver.Chrome(
            service=self.service, options=self.options)
        self.driver.get(
            'https://datalab.naver.com/shoppingInsight/sCategory.naver')

        for key in list(self.xpath_dict.keys())[:9]:
            xpath = self.xpath_dict[key]
            self._click(xpath=xpath)

        for xpath in self.xpath_dict['age']:
            self._click(xpath=xpath)

        xpath = self.xpath_dict['search']
        self._click(xpath=xpath)
        time.sleep(2)

        total_ls = []

        # 인기 검색어 리스트 20개 가져오기
        element = self.driver.find_element(By.XPATH, self.xpath_dict['top20'])
        data = element.text.split('\n')
        ls = list(zip(data[0::2], data[1::2]))
        total_ls += ls
        # print(ls[0])

        for _ in range(24):
            time.sleep(random.uniform(0.8, 1.2))
            # 다음 페이지 이동
            element = self.driver.find_element(
                By.XPATH, self.xpath_dict['next'])
            element.click()

            # 인기 검색어 리스트 20개 가져오기
            element = self.driver.find_element(
                By.XPATH, self.xpath_dict['top20'])
            data = element.text.split('\n')
            ls = list(zip(data[0::2], data[1::2]))
            total_ls += ls
            # print(ls[0])
            
        self.driver.close()
        return total_ls


if __name__ == '__main__':
    # py = TopKeyword()
    # print(py.run())
    