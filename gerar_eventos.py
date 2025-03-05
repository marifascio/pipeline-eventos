import json
import time
from faker import Faker
from google.cloud import pubsub_v1

# Configuração
project_id = "pipeline-eventos"
topic_id = "eventos"
publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_id)
fake = Faker()

def gerar_evento():
    return {
        "event_id": str(fake.uuid4()),
        "timestamp": fake.iso8601(),
        "user_id": str(fake.random_int(min=1000, max=9999)),
        "action": fake.random_element(elements=("click", "view", "purchase")),
        "platform": fake.random_element(elements=("web", "mobile", "tablet"))
    }

while True:
    evento = gerar_evento()
    data = json.dumps(evento).encode("utf-8") 
    publisher.publish(topic_path, data=data)
    print(f"Evento publicado: {evento}")
    time.sleep(1)
