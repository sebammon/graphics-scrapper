import codecs
import csv
import sys

import yaml
from bs4 import BeautifulSoup

PRODUCTS_TO_FIND = []
found_products = []

try:
    with open('./config.yml', 'r') as f:
        config = yaml.safe_load(f)
        products = config.get('products')

        if products is None:
            print('No products found in the `config.yml` file. See the README for the correct format.')
            sys.exit(1)
        else:
            PRODUCTS_TO_FIND = products
except FileNotFoundError:
    print('File `config.yml` not found. Reference the README for more information.')
    sys.exit(1)

try:
    with codecs.open('./page.html', 'r', 'utf-8') as page:
        print('>> SCRAPING WEBPAGE')

        html_doc = page.read()
        soup = BeautifulSoup(html_doc, 'html.parser')

        products = soup.find_all('div', {'class': 'main-info'})

        for product in products:
            title = product.find('h2').find('a').get_text().strip()
            price = product.find('p', {'class': 'special-price'}).find('span', {'class': 'price'}).get_text().strip()

            for product_to_find in PRODUCTS_TO_FIND:
                if product_to_find in title:
                    found_products.append({'title': title, 'price': price})
                    break
except FileNotFoundError:
    print(
        'File `page.html` not found. Please save the webpage as an HTML file to this folder.' +
        'Read the README for more information.')
    sys.exit(1)

print('>> WRITING TO CSV')

with open('./products.csv', 'a') as file:
    writer = csv.writer(file)

    for product in found_products:
        writer.writerow([product['title'], product['price']])

print('>> DONE')
