from parsing_base import Parser
import sys
import os
from bs4 import BeautifulSoup
import time
import pickle


class DealByParser(Parser):
    URL_SELLER = 'https://minsk.deal.by/opinions/list/'
    SELLERS_IDS = 500000

    def __init__(self):
        super().__init__()
        self.sellers = []
        self.last_seller_ids = int()

    def update_sellers(self):
        self.sellers = self.load_object('sellers')
        parsed_maximum = max([seller.id for seller in self.sellers])
        for id in range(self.SELLERS_IDS):
            if id <= parsed_maximum:
                continue
            url = self.URL_SELLER + str(id)
            print(url)
            resp = self.request_with_cookie(url)
            if resp.status_code == 404:
                continue
            seller = Seller(id)
            seller.deal_text = resp.text
            print(seller)
            self.sellers.append(seller)
        self.save_object(self.sellers, 'sellers')

    def save_sellers_from_html(self):
        sellers = []
        for html in os.listdir('html_files'):
            id = int(html.split('.')[0])
            seller = Seller(id)
            seller.update_deal_text_from_html()
            sellers.append(seller)
        self.save_object(sellers, 'sellers')


        # for url in check_sellers_list:
        #     print(url)
        #     if f"{url.split('/')[-1]}.html" in os.listdir('html_files'):
        #         self.sellers.append(Seller(url.split('/')[-1]))
        #         continue
        #     if int(url.split('/')[-1]) < parsed_maximum:
        #         continue
        #     resp = self.request_with_cookie(url)
        #     if resp.status_code == 404:
        #         continue
        #     self.save_html(resp.text, f"{url.split('/')[-1]}.html")
        #     self.sellers.append(Seller(url.split('/')[-1]))

    def request_with_cookie(self, url):
        headers = self.request.headers
        while True:
            resp = self.request.get(url, headers)
            if resp.status_code == 429:
                self.save_object(self.sellers, 'sellers')
                headers['Cookie'] = input('Пройти рекапчу и ввести куки')
            else:
                break
        return resp

    def update_dop_page_in_sellers(self):
        for seller in self.sellers:
            if seller.html_file in os.listdir('html_files'):
                continue
            seller.update_url_seller()
            resp = self.request_with_cookie(seller.url_seller)
            self.save_html(resp.text, f"{seller.id}_1.html")


class Seller:
    def __init__(self, id):
        self.id = id
        self.deal_url = f'https://minsk.deal.by/opinions/list/{id}'
        self.deal_text = str()
        self.name = str()
        self.url_seller = str()
        self.phones = []
        self.emails = []

    def read_html(self, file_name):
        with open(f'html_files/{file_name}', 'r', encoding='utf8') as file:
            return file.read()

    def update_deal_text_from_html(self):
        self.deal_text = self.read_html(f"{self.id}.html")
        # soup = BeautifulSoup(self.deal_text, 'lxml')
        # self.url_seller = soup.select_one('a.x-company-info__name')['href']

    def update_info(self):
        pass


if __name__ == '__main__':
    parser = DealByParser()
    # parser.save_sellers_from_html()
    parser.update_sellers()

