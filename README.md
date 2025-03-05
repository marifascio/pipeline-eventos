# 📊 Pipeline de Eventos com Airflow e BigQuery  

Este projeto automatiza a coleta, transformação e análise de eventos do site utilizando **Apache Airflow**, **Google Cloud Storage (GCS)** e **BigQuery**.

---

## 📁 Estrutura do Projeto

``` sh
pipeline-eventos/
│── dags/                   # DAGs do Airflow
│   ├── bq_pipeline_dag.py
│   ├── etl_vendas.py
│
│── scripts/                # Scripts auxiliares
│   ├── gerar_eventos.py
│   ├── publicar_mensagens.py
│
│── data/                   # Arquivos de dados
│   ├── vendas.csv
│   ├── website_logs.csv
│
│── configs/                # Configurações (NÃO COMMITAR)
│
│── .gitignore              # Arquivos ignorados pelo Git
│── requirements.txt        # Dependências do projeto
│── README.md               # Documentação do projeto
```

---

## 🔥 Tecnologias Utilizadas

- **Apache Airflow** – Orquestração do pipeline  
- **Google Cloud Platform (GCP)** – BigQuery e Cloud Storage  
- **Python** – Scripts de processamento e ingestão  
- **Google Pub/Sub** – Streaming de mensagens\

---

## 🎯 Objetivo do Projeto

1. **Coletar dados de eventos do site** (CSV no GCS).  
2. **Ingerir os dados no BigQuery** automaticamente via Airflow.  
3. **Executar consultas analíticas** sobre acessos ao site.  
4. **Automatizar o fluxo de dados** e garantir escalabilidade.  

---

## ⚙️ Como Executar o Projeto

### 1️⃣ **Configurar o Ambiente**
Clone este repositório e crie um ambiente virtual:

```sh
git clone https://github.com/marifascio/pipeline-eventos.git
cd pipeline-eventos
python -m venv airflow_venv
source airflow_venv/bin/activate  # Linux/Mac
airflow_venv\Scripts\activate     # Windows
```

Instale as dependências:

```sh
pip install -r requirements.txt
```

### 2️⃣ **Configurar o Airflow**
Inicialize o banco de dados:

```sh
airflow db init
```

Crie um usuário admin:

```sh
airflow users create \
    --username admin \
    --password admin \
    --firstname user \
    --lastname admin \
    --role Admin \
    --email example@mail.com
```

Inicie o Airflow:

```sh
airflow webserver --port 8080
airflow scheduler
```

Acesse http://localhost:8080 e ative a DAG bq_pipeline_dag.

## 📊 Exemplo de Query no BigQuery

``` sql
SELECT device_type, COUNT(*) AS total_acessos
FROM `meu-projeto-bigquery-452219.website_data.website_logs`
GROUP BY device_type
ORDER BY total_acessos DESC;
```

## ⚠️ **Importante**
-  NÃO COMMITAR credenciais (chave.json, .env) para o GitHub.
-  Utilizar variáveis de ambiente para armazenar credenciais.
-  Configurar permissões no GCP para execução do pipeline.

## ✨ **Autora**
- 👩‍💻 Mariana Fascio
- 📧 marianafascio@gmail.com
- 🌎 LinkedIn: **https://www.linkedin.com/in/marianafascio/**

