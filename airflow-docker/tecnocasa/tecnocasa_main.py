import logging
from scrape_master_url import scrape_url_master
from airflow.exceptions import AirflowException

def scrape_tecnocasa_url():
    try:
        tecnocasa_url = "https://www.tecnocasa.it/annunci/immobili/lombardia/milano.html"
        logging.info(f"Starting to scrape {tecnocasa_url}")
        scraped_annuncio_items = scrape_url_master(tecnocasa_url)
        logging.info(f"Scraping successful: {scraped_annuncio_items}")
        return scraped_annuncio_items
        
    except Exception as e:
        logging.error(f"Error while scraping {tecnocasa_url}: {str(e)}")
        raise AirflowException(f"Error while scraping {tecnocasa_url}: {str(e)}")
