import random
import json
import time

from paho.mqtt.client import Client

# Задаем параметры брокера
broker = 'mqtt.cloud.yandex.net'
port = 8883
topic = "$registries/arev7mm0e3m31r168s15/events"
# Генерируем уникальный идентификатор клиента
client_id: str = "CAD"
# Задаем учетные данные для подключения (если требуется)
username = 'are7rv1teba54fc08l1e'
password = '!iC3d8O%a0uq9QT1'


def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("Connected to MQTT Broker!")
    else:
        print(f"Failed to connect, return code {rc}")


def connect_mqtt() -> Client:
    client = Client(client_id)
    # Установка учетных данных (если требуется)
    client.username_pw_set(username, password)
    # Установка обработчика соединения
    client.on_connect = on_connect
    # Подключение к брокеру
    client.connect(broker, port)
    return client


def publish(client: Client):
    # Генерация данных для отправки
    data_to_send = {
        "PM2_5": "37.0",
        "PM10": "41.8"
    }
    # Преобразование данных в формат JSON
    payload = json.dumps(data_to_send)
    # Отправка данных
    client.publish(topic, payload=payload, qos=1)
    print("Data sent successfully")


if __name__ == '__main__':
    client = connect_mqtt()
    client.loop_start()  # Запуск цикла обработки событий в отдельном потоке
    publish(client)  # Отправка данных
    time.sleep(2)  # Пауза для завершения отправки данных
    client.loop_stop()  # Остановка цикла обработки событий
    client.disconnect()  # Отключение от брокера
