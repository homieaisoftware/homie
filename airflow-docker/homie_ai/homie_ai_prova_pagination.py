import logging
import json
import csv
from bs4 import BeautifulSoup
import requests

url = f'https://www.immobiliare.it/vendita-case/milano-provincia/?criterio=rilevanza&prezzoMinimo=10000&prezzoMassimo=20000&pag=2'
response = requests.get(url)
if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')
    pagination_list = soup.find('div', class_='in-pagination__list')
    if pagination_list:
        max_page = max([int(a.text) for a in pagination_list.find_all('a', class_='in-pagination__item') if a.text.isdigit()])
        print(max_page) 