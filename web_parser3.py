import requests
import os
import time
import json

from bs4 import BeautifulSoup
from requests import cookies
from requests.api import head
from scrapy_user_agents import user_agent_picker

from abstract_page import AbstractPage


def get_data(url:str):

    headers = {
        "accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "accept-encoding":"gzip, deflate, br",
        "accept-language":"ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        "sec-ch-ua-platform":"Windows",
        "user-agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"
    }

    cookies_jar = requests.get(url, headers=headers).cookies
    
    for i in range(2, 16):
        
        url = f"https://lovemylife.nsp25.md/shop/page/{i}"
        # response = requests.get(url=url, headers=headers, cookies=cookies_jar)
        # time.sleep(1)

        folder_path = f"C:/Users/nichi/Projects/WebParser/lesson3/data/page_{i}"
        page_source_path = folder_path + f"/page_{i}.html"
        data_path = folder_path + f"/data_{i}.json"

        # os.mkdir(folder_path)
        # with open(page_source_path, 'w', encoding="utf-8") as file:
        #     file.write(response.text)

        with open(page_source_path, 'r', encoding="utf-8") as file:
            soup = BeautifulSoup(file.read(), 'lxml')

        with open(data_path, 'w', encoding="utf-8") as file:
            
            # find all products
            product_container_list = soup.find_all('div', class_='card__container')
            
            # .card__image>img            (img url)
            # 'h6', class_=card__title    (name)
            # .card__link                 (url)
            # .card__additional-info>span:first-of-type  (id)
            # .card__price                (price div container)
            
            final_product_list = []
            for container in product_container_list:
                
                product_id = container.select_one('.card__additional-info>span:first-of-type').text
                img_url = container.select_one('.card__image>img')['src']
                product_name = container.find('h6', class_='card__title').text
                product_url = container.select_one('.card__link')['href']
                price = None

                price_sale = container.select_one('.card__price>ins')
                if price_sale:
                    price = price_sale.text
                else:
                    price = container.select_one('.card__price>span').text
                
                product_dict = {
                    'ID':product_id,
                    'name':product_name.replace("\n",""),
                    'url':product_url,
                    'img_url':img_url,
                    'price':price
                }
                
                final_product_list.append(product_dict)
            
            json.dump(final_product_list, file, indent=4, ensure_ascii=False)


def main():
    get_data("https://lovemylife.nsp25.md/shop")


if __name__ == "__main__":
    main()