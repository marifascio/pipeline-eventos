from google.cloud import bigquery
import pandas as pd

# 🟢 Configurações
PROJETO_ID = "meu-projeto-bigquery-452219" 
DATASET_ID = "website_data"
TABELA_ID = "website_logs"
TABELA_COMPLETA = f"{PROJETO_ID}.{DATASET_ID}.{TABELA_ID}"

# 🟢 Inicializa o cliente do BigQuery
client = bigquery.Client()

# 🟡 Criar o dataset
dataset_ref = client.dataset(DATASET_ID)
try:
    client.get_dataset(dataset_ref)
    print(f"✅ Dataset '{DATASET_ID}' já existe.")
except Exception:
    dataset = bigquery.Dataset(dataset_ref)
    dataset.location = "US"
    client.create_dataset(dataset)
    print(f"✅ Dataset '{DATASET_ID}' criado com sucesso.")

# 🟡 Criar a tabela no BigQuery
schema = [
    bigquery.SchemaField("user_id", "STRING"),
    bigquery.SchemaField("timestamp", "TIMESTAMP"),
    bigquery.SchemaField("page_visited", "STRING"),
    bigquery.SchemaField("device_type", "STRING"),
]

table_ref = client.dataset(DATASET_ID).table(TABELA_ID)
try:
    client.get_table(table_ref)
    print(f"✅ Tabela '{TABELA_ID}' já existe.")
except Exception:
    table = bigquery.Table(table_ref, schema=schema)
    client.create_table(table)
    print(f"✅ Tabela '{TABELA_ID}' criada com sucesso.")

# 🟡 Carregar dados do CSV para o BigQuery
df = pd.read_csv("website_logs.csv")

job_config = bigquery.LoadJobConfig(
    schema=schema,
    source_format=bigquery.SourceFormat.CSV,
    skip_leading_rows=1,  # Ignora o cabeçalho do CSV
    write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE  # Substitui os dados existentes
)

with open("website_logs.csv", "rb") as arquivo:
    job = client.load_table_from_file(arquivo, TABELA_COMPLETA, job_config=job_config)

job.result()  # Aguarda o carregamento finalizar

print(f"✅ {job.output_rows} registros carregados na tabela '{TABELA_COMPLETA}'.")

# 🔵 Executar consulta no BigQuery
query = f"""
SELECT device_type, COUNT(*) AS total_acessos
FROM `{TABELA_COMPLETA}`
GROUP BY device_type
ORDER BY total_acessos DESC;
"""

query_job = client.query(query)
df_resultado = query_job.to_dataframe()

print("\n📊 Resultado da Análise:")
print(df_resultado)
