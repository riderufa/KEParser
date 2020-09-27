import json
import time
import csv

import requests


URL1 = 'https://kazanexpress.ru/api/main/more?categoryId=1433&size=20&page='
URL2 = '&sortBy=&order=ascending'
HEADERS = {
    'authorization': 'Basic a2F6YW5leHByZXNzLWN1c3RvbWVyOmN1c3RvbWVyU2VjcmV0S2V5',
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Mobile Safari/537.36',
    'accept': '*/*'
}


def get_html(data_url, params=None):
    session = requests.Session()
    session.headers = HEADERS
    response = session.get(data_url)
    return response


def parse_shampoo():
    pages_count = 4
    products = []
    for page in range(1, pages_count + 1):
        print(f'Парсинг страницы {page} из {pages_count}')
        time.sleep(1)
        html = get_html(URL1 + str(page) + URL2)
        if html.status_code == 200:
            parsed_products = json.loads(html.text)
            for item in parsed_products['payload']:
                product = {
                    'title': item['title'],
                    'price': item['sellPrice'],
                    'orders': item['ordersQuantity'],
                    'rating': item['rating']
                }
                products.append(product)
            with open('products.json', 'w') as outfile:
                json.dump(products, outfile)
            with open('products.csv', 'w', newline='') as file:
                writer = csv.writer(file, delimiter=';')
                writer.writerow(['Наименование', 'Стоимость', 'Количество заказов', 'Рейтинг'])
                for item in products:
                    writer.writerow([item['title'], item['price'], item['orders'], item['rating']])
        else:
            print('Error')


parse_shampoo()
