import json
import time
import ssl
from datetime import datetime
from paho.mqtt.client import Client
from serial_example import *

# Задаем параметры брокера MQTT
broker_address = "mqtt.cloud.yandex.net"
port = 8883
topic = "$registries/arev7mm0e3m31r168s15/events"
qos = 1

# Задаем учетные данные для подключения
device_id = "are7rv1teba54fc08l1e"
password = "!iC3d8O%a0uq9QT1"

# Путь к CA сертификату
ca_cert_path = "rootCA.crt"
# /dev/ttyUSB0

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
    else:
        print(f"Failed to connect, return code {rc}")


def connect_mqtt():
    client = Client(client_id="CAD")
    # Установка учетных данных
    client.username_pw_set(username=device_id, password=password)
    # Установка обработчика соединения
    client.on_connect = on_connect
    # Настройка TLS
    client.tls_set(ca_certs=ca_cert_path, tls_version=ssl.PROTOCOL_TLSv1_2)
    # Подключение к брокеру
    client.connect(broker_address, port)
    return client


def generate_timestamp():
    # Генерация временной метки в формате ISO 8601
    return datetime.now().isoformat() + "Z"


def transform_data(serial_data):
    # Парсинг данных из serial формата
    pm25_value = serial_data.get("PM2_5", None)
    pm10_value = serial_data.get("PM10", None)
    pressure_pa = serial_data.get("pressure_pa", None)
    altitude_m = serial_data.get("altitude_m", None)
    temperature_c = serial_data.get("temperature_c", None)
    latitude = serial_data.get("latitude", None)
    longitude = serial_data.get("longitude", None)

    # Создание словаря для нового формата данных
    data_to_send = {
        "device_timestamp": generate_timestamp(),  # Генерация временной метки
        "device_name": "device_33",
        "sensor_model": "sds011",
        "location": [{"latitude": latitude}, {"longitude": longitude}],
        "sensordatavalues": [
            {"value_type": "PM2_5", "value": pm25_value},
            {"value_type": "PM10", "value": pm10_value},
            {"value_type": "pressure_pa", "value": pressure_pa},
            {"value_type": "altitude_m", "value": altitude_m},
            {"value_type": "temperature_c", "value": temperature_c}
        ]
    }

    return data_to_send


def publish(client, serial_data):
    # Преобразование данных
    data_to_send = transform_data(serial_data)

    # Преобразование данных в формат JSON
    payload = json.dumps(data_to_send)

    # Отправка данных
    client.publish(topic, payload=payload, qos=qos)
    print("Data sent successfully")


def run():
    flush()
    while True:
        # time.sleep(2)
        client = connect_mqtt()
        client.loop_start()

        # Данные из serial
        # serial_data = {
        #     "PM2_5": "300.8",
        #     "PM10": "300.5",
        #     "pressure_pa": "91096.83",
        #     "altitude_m": "29.01",
        #     "temperature_c": "29.08",
        #     "latitude": "73.296441",
        #     "longitude": "53.100502"
        # }
        serial_data = get_json()
        if serial_data is not None:
            serial_data["latitude"]  = "73.296441"
            serial_data["longitude"] = "53.100502"
            
            # Отправка данных
            publish(client, serial_data)

            time.sleep(2)
      # Пауза для завершения отправки данных
    client.loop_stop()  # Остановка цикла обработки событий
    client.disconnect()  # Отключение от брокера


if __name__ == '__main__':
    run()
