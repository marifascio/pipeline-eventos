from google.cloud import pubsub_v1
import json
import time

# Substitua pelo seu tópico do Pub/Sub
PROJECT_ID = "pipeline-eventos"
TOPIC_ID = "eventos"

# Função para publicar uma mensagem no Pub/Sub
def publish_message(publisher, topic_path, data):
    try:
        # Converte a mensagem em bytes
        message_data = json.dumps(data).encode("utf-8")
        
        # Publica a mensagem
        future = publisher.publish(topic_path, data=message_data)
        print(f"Mensagem publicada com ID: {future.result()}")
    except Exception as e:
        print(f"Erro ao publicar mensagem: {e}")

# Configuração principal
def main():
    # Inicializa o cliente Publisher
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(PROJECT_ID, TOPIC_ID)

    # Exemplo de mensagens a serem enviadas
    mensagens = [
        {"event_id": "123", "timestamp": "2024-12-17T22:00:00Z", "user_id": "456", "action": "click", "platform": "web"},
        {"event_id": "124", "timestamp": "2024-12-17T22:05:00Z", "user_id": "457", "action": "purchase", "platform": "mobile"},
        {"event_id": "125", "timestamp": "2024-12-17T22:10:00Z", "user_id": "458", "action": "signup", "platform": "desktop"}
    ]

    # Loop para publicar mensagens automaticamente
    for mensagem in mensagens:
        publish_message(publisher, topic_path, mensagem)
        time.sleep(1)  # Aguarda 1 segundo entre as publicações (opcional)

if __name__ == "__main__":
    main()
