import base64
import json
import os
import logging
from typing import Dict, Any, Optional
from google.cloud import bigquery
from tenacity import retry, stop_after_attempt, wait_exponential

os.environ["GOOGLE_CLOUD_PROJECT"] = "pipeline-eventos"  # ID do projeto GCP

# Configuração
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
client = bigquery.Client()
TABLE_ID = "pipeline-eventos.eventos.eventos_processados"

def decode_message(event: Dict[str, Optional[Any]]) -> Dict[str, Any]:
    """
    Decodifica a mensagem Pub/Sub do formato base64 e converte para JSON.
    """
    if 'data' not in event:
        raise ValueError("O campo 'data' está ausente no evento.")
    
    try:
        mensagem = base64.b64decode(event['data']).decode('utf-8')
        if len(mensagem) > 1024:
            raise ValueError("Mensagem excede o tamanho máximo permitido.")
        return json.loads(mensagem)
    except (json.JSONDecodeError, ValueError) as e:
        raise ValueError(f"Erro ao decodificar ou converter a mensagem: {e}")

def validate_event(evento: Dict[str, Any]) -> Dict[str, Any]:
    """
    Valida e retorna os campos esperados do evento.
    """
    campos_obrigatorios = ["event_id", "timestamp", "user_id", "action", "platform"]
    for campo in campos_obrigatorios:
        if campo not in evento:
            raise ValueError(f"Campo obrigatório ausente: {campo}")
    
    return {
        "event_id": evento["event_id"],
        "timestamp": evento["timestamp"],
        "user_id": evento["user_id"],
        "action": evento["action"],
        "platform": evento["platform"]
    }

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=2))
def inserir_no_bigquery(dados: Dict[str, Any]):
    """
    Insere dados validados no BigQuery.
    """
    try:
        print(f"Dados sendo enviados ao BigQuery: {dados}")
        erros = client.insert_rows_json(TABLE_ID, [dados])
        if erros:
            raise Exception(f"Erros ao inserir no BigQuery: {erros}")
        print("Evento inserido com sucesso no BigQuery.")
    except Exception as e:
        print(f"Erro ao inserir no BigQuery: {e}")
        raise


def processar_eventos(event, context):
    """
    Função acionada pelo Pub/Sub para processar eventos e salvar no BigQuery.
    """
    print(f"Evento recebido: {event}")  # Log para debugging
    try:
        # Decodificar a mensagem
        mensagem_decodificada = decode_message(event)
        print(f"Mensagem decodificada: {mensagem_decodificada}")
        
        # Validar mensagem
        evento_validado = validate_event(mensagem_decodificada)
        print(f"Evento validado: {evento_validado}")
        
        # Inserir no BigQuery
        inserir_no_bigquery(evento_validado)
    
    except ValueError as ve:
        print(f"Erro de validação ou decodificação: {ve}")
    except Exception as e:
        print(f"Erro inesperado: {e}")
    
    print("Processamento concluído.")