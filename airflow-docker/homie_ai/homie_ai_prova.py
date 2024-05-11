
import logging
import json
import csv
from bs4 import BeautifulSoup
import requests
class HomieAI:
    def __init__(self, base_url, total_max_price=1000000,max_price=10000,current_page=1,min_price=0, output_file='homie_ai/lista_immobili_immobiliare.csv'):
        self.base_url = base_url
        self.total_max_price = total_max_price
        self.max_price= max_price
        self.min_price=min_price
        self.current_page=current_page
        self.output_file = output_file
        self.fieldnames = ['agency', 'real_estate_agent', 'price', 'price_range',
                           'bathrooms', 'bedrooms', 'elevator', 'visibility',
                           'type_id', 'type', 'garage', 'floor_appartment', 'floor_appartment',
                           'floors_buildings', 'surface', 'category_label', 'category_description',
                           'energy', 'features', 'latitude', 'longitude', 'nation_id', 'nation',
                           'province', 'region', 'macrozone', 'microzone', 'city']

    def scrape_immobiliare_data(self):

        with open(self.output_file, 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.fieldnames)
            writer.writeheader()
            
            while self.min_price < self.total_max_price:
                self.current_page=1
                logging.debug("Parsing the content using BeautifulSoup for range {self.min_price} to {self.max_price}")
                url = f'{self.base_url}/?criterio=rilevanza&prezzoMinimo={self.min_price}&prezzoMassimo={self.max_price}&pag={self.current_page}'
                response = requests.get(url)
                soup_price = BeautifulSoup(response.content, 'html.parser')
                pagination_list = soup_price.find('div', class_='in-pagination__list')
                if pagination_list:
                    max_page = max([int(a.text) for a in pagination_list.find_all('a', class_='in-pagination__item') if a.text.isdigit()])
                    current_page = self.current_page + 1
                    while current_page < max_page:
                        url_pagine =f'{self.base_url}/?criterio=rilevanza&prezzoMinimo={self.min_price}&prezzoMassimo={self.max_price}&pag={current_page}'
                        logging.debug("Parsing the content using BeautifulSoup")
                        response_pagine = requests.get(url_pagine)
                        if response.status_code == 200:
                                soup_pagine = BeautifulSoup(response_pagine.content, 'html.parser')
                    
                        script_tag = soup_pagine.find('script', id='__NEXT_DATA__', type='application/json')
                        if script_tag:
                            # Extract the JSON data from the script tag
                            json_data = json.loads(script_tag.string)

                        # Access the desired data within the JSON hierarchy
                            properties = json_data['props']['pageProps']['dehydratedState']['queries'][0]['state']['data']
                            inmuebles = properties['results']

                        # Iteramos sobre cada inmueble
                            for inmueble in inmuebles:
                            # Accedemos a la información del inmueble
                                real_estate_info = inmueble['realEstate']

                            # Accedemos a la información del anunciante
                                advertiser_info = real_estate_info.get('advertiser', {})
                                floor= real_estate_info.get('floor',{})
                                floor_appartment = floor.get('Abbreviation','')

                                # Accedemos a la información de la agencia
                                agency_info = advertiser_info.get('agency', {})

                            # Obtenemos el nombre de la agencia
                                agency_name = agency_info.get('displayName', '')

                            # Creamos un diccionario para guardar la información del inmueble
                                inmueble_info = {
                                'agency': agency_name,
                                'real_estate_agent': real_estate_info['advertiser'].get('supervisor', ''),
                                'price': real_estate_info['price'].get('value'),
                                'price_range': real_estate_info['price'].get('priceRange'),
                                'bathrooms': real_estate_info['properties'][0].get('bathrooms', ''),
                                'bedrooms': real_estate_info['properties'][0].get('bedRoomsNumber'),
                                'elevator': real_estate_info['properties'][0].get('elevator', ''),
                                'visibility': real_estate_info['properties'][0].get('visibility', ''),
                                'type_id': real_estate_info['properties'][0]['typology']['id'],
                                'type': real_estate_info['properties'][0]['typology']['name'],
                                'garage': real_estate_info['properties'][0].get('ga4Garage', ''),
                                'floor_appartment':floor_appartment,
                                'floors_buildings': real_estate_info['properties'][0].get('floors', ''),
                                'surface': real_estate_info['properties'][0].get('surface'),
                                'category_label': real_estate_info['properties'][0]['category']['id'],
                                'category_description': real_estate_info['properties'][0]['category']['name'],
                                'energy': real_estate_info['properties'][0].get('energy'),
                                'features': real_estate_info['properties'][0].get('features'),
                                'latitude': real_estate_info['properties'][0]['location']['latitude'],
                                'longitude': real_estate_info['properties'][0]['location']['longitude'],
                                'nation_id': real_estate_info['properties'][0]['location']['nation']['id'],
                                'nation': real_estate_info['properties'][0]['location']['nation']['name'],
                                'province': real_estate_info['properties'][0]['location']['province'],
                                'region': real_estate_info['properties'][0]['location']['region'],
                                'macrozone': real_estate_info['properties'][0]['location']['macrozone'],
                                'microzone': real_estate_info['properties'][0]['location']['microzone'],
                                'city': real_estate_info['properties'][0]['location']['city']
                            }

                            # Escribimos la información del inmueble en una nueva línea del CSV
                                writer.writerow(inmueble_info)
                                logging.info("Finished writing page {} to csv file".format(str(current_page)))

                        current_page += 1
                self.min_price= self.max_price
                self.max_price =self.max_price +10000


# Uso de la clase HomieAI
homie = HomieAI(base_url='https://www.immobiliare.it/vendita-case/milano-provincia/?criterio=rilevanza&')
homie.scrape_immobiliare_data()