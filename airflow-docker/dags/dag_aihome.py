from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import PythonOperator
from datetime import datetime
from homie_ai.homie_ai import HomieAI

default_args = {
    'start_date': datetime.now(),
    'retries': 0,
}

def homie_immobiliare_url():
    homie = HomieAI(base_url='https://www.immobiliare.it/vendita-case/milano-provincia/?criterio=rilevanza&')
    homie.scrape_immobiliare_data()

with DAG('HOMIE_AI', default_args=default_args, schedule_interval=None) as dag:
    start = DummyOperator(
        task_id='start'
    )

    scrape_immobiliare_data = PythonOperator(
        task_id='scrape_immobiliare_data',
        python_callable=homie_immobiliare_url
    )

    start >> scrape_immobiliare_data
