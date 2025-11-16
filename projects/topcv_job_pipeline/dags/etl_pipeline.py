import sys
from pathlib import Path
import pendulum
from airflow import DAG
from airflow.operators.python import PythonOperator
from app.crawl_data import crawl_to_list
from app.transform_data import transform_data_cleaned
from app.load_data import load_data_to_sql
from datetime import datetime

dag_path = Path(__file__).parent.absolute()
project_root = dag_path.parent
sys.path.append(str(project_root))

default_args = {
    "start_date": datetime(2024, 1, 1),
}


dag = DAG(
    "etl_topcv_pipeline",
    schedule_interval="@daily",
    default_args=default_args,
    catchup=False
)

def task_crawl(**context):
    qtpl = "https://www.topcv.vn/tim-viec-lam-data-analyst?type_keyword=1&sba=1&page={page}"
    raw_data = crawl_to_list(query_url_template=qtpl, start_page=1, end_page=1, delay_between_pages=(0.5, 1))
    context["ti"].xcom_push(key="raw_jobs", value=raw_data)

def task_transform(**context):
    raw_records = context["ti"].xcom_pull(key="raw_jobs", task_ids="crawl_task") or []
    if raw_records:
        clean_data = transform_data_cleaned(raw_records)
        context["ti"].xcom_push(key="clean_jobs", value=clean_data)

def task_load(**context):
    clean_records = context["ti"].xcom_pull(key="clean_jobs", task_ids="transform_task") or []
    if clean_records:
        load_data_to_sql(clean_records)

crawl_task = PythonOperator(task_id="crawl_task", python_callable=task_crawl, dag=dag)
transform_task = PythonOperator(task_id="transform_task", python_callable=task_transform, dag=dag)
load_task = PythonOperator(task_id="load_task", python_callable=task_load, dag=dag)

crawl_task >> transform_task >> load_task