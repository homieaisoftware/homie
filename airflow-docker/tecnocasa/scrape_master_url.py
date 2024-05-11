import os
import logging
import requests
from bs4 import BeautifulSoup
import pandas as pd
from scrape_html_childs import scrape_multiple_urls, scrape_html_files, scrape_url_immobiliare, save_to_txt

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def scrape_url_master(url):
    try:
        response = None  # Initialize response outside the if blocks
        if 'tecnocasa' in url:
            logging.info(f"Sending HTTP GET request to {url}")
            response = requests.get(url)
            logging.info(f"Got response from HTTP request: {response.status_code}")
            if response.status_code == 200:
                logging.info('Correctly detected tecnocasa url')
                output_folder = r"/opt/airflow/tecnocasa/tecnocasa-output-files"
                if not os.path.exists(output_folder):
                    os.makedirs(output_folder)
                    logging.info(f"Output folder set to {output_folder}")
                soup = BeautifulSoup(response.content, 'html.parser')
                logging.debug("Parsing the content of {url}")

            template_tag = soup.find('template', attrs={'slot': 'cities-seo-list'})
                    # Scrape data from the listed URLs and create files for each URL
    # Get a list of all the files in the directory
            if template_tag:
                logging.debug("Get Urls from further scrapping")
                cities_spans = template_tag.find_all('span')
                urls = [span.a['href'] for span in cities_spans if span.a]
                file_path = r'/opt/airflow/tecnocasa/tecnocasa-output-files/urls_to_scrape_tecnocasa.txt'
                save_to_txt(file_path, urls)
                logging.info("Correctly created txt of childs urls")
                results_scrapper =scrape_html_files(scrape_multiple_urls(file_path))
                combined_data = {}
                    
                for data in results_scrapper:
                    for key, value in data.items():
                        combined_data.setdefault(key, []).extend(value)
                df = pd.DataFrame(combined_data)
                df.drop_duplicates(inplace=True)
                #output_csv = os.path.join(, "tecnocasa.csv")
                df.to_csv('/opt/airflow/tecnocasa/tecnocasa-output-files/data_tecnocasa.csv', index=False)
                logging.debug("Data saved to CSV")

        elif 'immobiliare' in url:
            all_data = []
            max_pages = 1000
            output_folder = 'Immobiliare'
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)
            for page in range(1, max_pages + 1):
                url_to_scrape = f'{url}{page}'
                logging.debug(f"Sending HTTP GET request to {url}")
                response = requests.get(url_to_scrape)
                immobiliare_info = scrape_url_immobiliare(url_to_scrape, response, page)
                
                if immobiliare_info is not None:
                    all_data.extend(immobiliare_info)

                if all_data:
                    df = pd.DataFrame(all_data)
                    df.to_csv('Immobiliare/immobiliare_clean.csv', index=False)
                    logging.debug("Immobiliare data saved to CSV")

    except Exception as e:
        logging.error(f"Error while scraping {url}: {str(e)}")
        raise