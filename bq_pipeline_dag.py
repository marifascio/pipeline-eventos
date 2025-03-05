from airflow import DAG
from airflow.providers.google.cloud.operators.bigquery import BigQueryInsertJobOperator
from airflow.utils.dates import days_ago
from datetime import timedelta

# Configurações do GCP
PROJECT_ID = "meu-projeto-bigquery-452219"
DATASET_ID = "website_data"
TABLE_ID = "website_logs"
BUCKET_NAME = "bucket-website-logs"
CSV_FILE = "website_logs.csv"
TABLE_PATH = f"{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}"

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": days_ago(1),
    "email_on_failure": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

dag = DAG(
    "bq_pipeline_dag",
    default_args=default_args,
    description="Pipeline ELT no Cloud Composer 3 em us-east1",
    schedule_interval="0 6 * * *",  # Executa diariamente às 06:00 UTC
    catchup=False,
)

# 🔹 Tarefa: Carregar os dados do CSV para o BigQuery

load_to_bq = BigQueryInsertJobOperator(
    task_id="load_data_to_bq",
    configuration={
        "load": {
            "destinationTable": {
                "projectId": PROJECT_ID,
                "datasetId": DATASET_ID,
                "tableId": TABLE_ID,
            },
            "sourceUris": [f"gs://{BUCKET_NAME}/{CSV_FILE}"],
            "sourceFormat": "CSV",
            "skipLeadingRows": 1,
            "writeDisposition": "WRITE_TRUNCATE",  
            "autodetect": True,  
        }
    },
    dag=dag,
)


# 🔹 Tarefa: Executar query no BigQuery
query_bq = BigQueryInsertJobOperator(
    task_id="query_bq",
    configuration={
        "query": {
            "query": f"""
                SELECT device_type, COUNT(*) AS total_acessos
                FROM `{TABLE_PATH}`
                GROUP BY device_type
                ORDER BY total_acessos DESC
            """,
            "useLegacySql": False,
        }
    },
    dag=dag,
)

# 🔹 Definir a sequência das tarefas
load_to_bq >> query_bq
