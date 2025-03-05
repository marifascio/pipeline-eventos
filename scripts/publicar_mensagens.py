import json
from google.cloud import pubsub_v1
from google.auth.exceptions import DefaultCredentialsError
import os

# 1. Configurar as credenciais do Google Cloud
# Use o caminho correto para o arquivo de credenciais
try:
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:/Users/escri/OneDrive/Documentos/chave.json"
    print(f"Variável de ambiente configurada: {os.environ['GOOGLE_APPLICATION_CREDENTIALS']}")
except KeyError as e:
    print("Erro ao configurar a variável de ambiente:", str(e))
    exit(1)

# 2. Configurar o tópico do Pub/Sub
PROJECT_ID = "pipeline-eventos"
TOPIC_ID = "eventos"

# 3. Criar mensagens de exemplo
mensagens = [
    {
        "event_id": "123",
        "timestamp": "2025-01-10T12:34:56Z",
        "user_id": "456",
        "action": "click",
        "platform": "web"
    },
    {
        "event_id": "124",
        "timestamp": "2025-01-10T12:35:56Z",
        "user_id": "457",
        "action": "view",
        "platform": "mobile"
    }
]

# 4. Publicar mensagens no Pub/Sub
def publicar_mensagens(project_id, topic_id, mensagens):
    """Publica mensagens em um tópico do Pub/Sub."""
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)
    print(f"Publicando mensagens no tópico: {topic_path}")

    for mensagem in mensagens:
        try:
            # Serializa a mensagem para JSON
            data = json.dumps(mensagem).encode("utf-8")
            # Publica a mensagem
            future = publisher.publish(topic_path, data=data)
            print(f"Mensagem publicada com sucesso: {mensagem['event_id']}")
        except Exception as e:
            print(f"Erro ao publicar mensagem {mensagem['event_id']}: {str(e)}")

# 5. Executar a função de publicação
if __name__ == "__main__":
    try:
        publicar_mensagens(PROJECT_ID, TOPIC_ID, mensagens)
    except DefaultCredentialsError as e:
        print(f"Erro de credenciais: {str(e)}. Verifique a configuração.")
    except Exception as e:
        print(f"Erro inesperado: {str(e)}")
