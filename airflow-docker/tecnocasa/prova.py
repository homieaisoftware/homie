import logging
from scrape_master_url import scrape_url_master

def scrape_tecnocasa_url(url):
    try:
        logging.info(f"Starting to scrape {url}")
        scraped_annuncio_items = scrape_url_master(url)
        return scraped_annuncio_items
    except Exception as e:
        logging.error(f"Error while scraping {url}: {str(e)}")
url ="https://www.tecnocasa.it/annunci/immobili/lombardia/milano.html"
scrape_tecnocasa_url(url)

