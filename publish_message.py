import json
from google.cloud import pubsub_v1

# Configuração do Pub/Sub
project_id = "pipeline-eventos"
topic_id = "eventos"
publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_id)

# Mensagem JSON correta
mensagem = {
    "event_id": "123",
    "timestamp": "2024-12-17T21:00:00Z",
    "user_id": "456",
    "action": "click",
    "platform": "web"
}

# Publicar mensagem
data = json.dumps(mensagem).encode("utf-8")  # Codificar mensagem em JSON
future = publisher.publish(topic_path, data=data)
print(f"Mensagem publicada com ID: {future.result()}")