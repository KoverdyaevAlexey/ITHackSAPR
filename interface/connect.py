import psycopg2
import json
def get_json():
    hostname = "rc1d-gh60uaznwt0p6gc1.mdb.yandexcloud.net"
    port = "6432"
    database = "telemetry"
    username = "guest"
    password = "BO1JXIZ&toSpG25A"
    ca_cert_path = "rootCA.crt"

    conn = psycopg2.connect(
        host=hostname,
        port=port,
        dbname=database,
        user=username,
        password=password,
        sslmode='verify-ca',
        sslrootcert=ca_cert_path
    )

    cur = conn.cursor()

    cur.execute("SELECT * FROM telemetry_hist")

    # Получение результатов
    rows = cur.fetchall()

    # Создание списка для хранения результатов в формате JSON
    result_json = []

    # Преобразование результатов в JSON
    for row in rows:
        # Парсинг строковых представлений JSON в Python-объекты
        location_json = json.loads(row[4])
        sensordatavalues_json = json.loads(row[5])

        # Создание объекта JSON для каждой строки результата
        row_json = {
            "device_timestamp": row[1],
            "device_name": row[2],
            "sensor_model": row[3],
            "location": location_json,
            "sensordatavalues": sensordatavalues_json
        }

        # Добавление объекта JSON в список результатов
        result_json.append(row_json)

    # Преобразование списка результатов в строку JSON
    result_json_str = json.dumps(result_json, ensure_ascii=False)

    # Закрытие курсора и соединения
    cur.close()
    conn.close()

    # # Вывод результата
    # print(result_json_str)


    # Предположим, у вас есть строка JSON
    # result_json_strjson_str = '{"device_timestamp": "2024-04-17T08:28:47.340Z", "device_name": "iot_test_device", "sensor_model": "sds011", "location": [{"latitude": "55.796441"}, {"longitude": "37.600502"}], "sensordatavalues": [{"value_type": "PM2_5", "value": "4.9"}, {"value_type": "PM10", "value": "7.1"}]}'

    # Разбираем строку JSON в объект Python
    data = json.loads(result_json_str)

    # Форматируем объект JSON с отступами для красивой визуализации
    pretty_json_str = json.dumps(data, indent=4)

    #print(pretty_json_str)
    # Выводим отформатированную строку JSON
    return pretty_json_str