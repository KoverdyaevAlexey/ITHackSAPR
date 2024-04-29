import folium.features
import streamlit as st
import numpy as np
import pandas as pd
import folium
from streamlit_folium import st_folium
import json
import math
from connect import get_json
import time
import threading
from datetime import datetime
class OEM:  
    def __init__(self):
        json_text = get_json()
        self.devices_data = json.loads(json_text)
        #print(self.devices_data)
        self.pm_2_5_gradation = [25, 35, 100, 500]
        self.pm_10_gradation = [30, 50, 75, 300]
        self.pm_gradation_color = ["#32a83e", "#e39312", "#de2007", "#8d0896"]
        self.prev_len = None
        self.curr_len = None
        self.device_names = []
        self.selected_device = None
        self.regions = {}
        self.map = None
        self.start_date = None
        self.start_time = None
        self.end_date = None
        self.end_time = None
        
    # Создание интерактивной карты
    def update_data(self):
        json_text = get_json()
        self.devices_data = json.loads(json_text)
        # Extracting latitude and longitude values
        #print(self.devices_data)
        self.curr_len = len(self.devices_data)
        
        if self.prev_len is None:
            self.prev_len = 0
        #if self.prev_len == 0:
        for data in self.devices_data:
            #print(F"DATAAA {data}")
            #print(data)
            #print(data)
            #print(type(data))
            device_name = data['device_name']
            if device_name not in self.device_names:
                self.device_names.append(device_name)
            #print(data['sensordatavalues'])
            device_timestamp = data['device_timestamp']
            latitude = float(data['location'][0]['latitude'])
            longitude = float(data['location'][1]['longitude'])

            try:
                pm2_5 = float(data['sensordatavalues'][0]['value'])
                pm10 = float(data['sensordatavalues'][1]['value'])
                pressure = float(data['sensordatavalues'][2]['value']) 
                altitude = float(data['sensordatavalues'][3]['value'])
                temperature = float(data['sensordatavalues'][4]['value'])
            except:
                pm2_5 = -1
                pm10 = -1
                pressure = -1
                altitude = -1
                temperature = -1
            pm_mean = (pm2_5 + pm10) / 2 
            for i in range(len(self.pm_2_5_gradation)):
                if pm_mean < self.pm_2_5_gradation[i]:
                    color = self.pm_gradation_color[i]
                    break
                    
            if (device_name) not in self.regions:
                self.regions[(device_name)] = {'pm2_5_values': [], 'pm10_values': [], 
                                                        'pressure_values' : [],
                                                         'altitude_values' : [],
                                                         'temperature_values' : [],
                                                        'color': [], 
                                                        'device_timestamp': [], 
                                                        'latitude' : [],
                                                        'longitude' : []}

            self.regions[(device_name)]['pm2_5_values'].append(pm2_5)
            self.regions[(device_name)]['pm10_values'].append(pm10)
            self.regions[(device_name)]['color'].append(color)
            self.regions[(device_name)]['device_timestamp'].append(device_timestamp)
            self.regions[(device_name)]['latitude'].append(latitude)
            self.regions[(device_name)]['longitude'].append(longitude)
            self.regions[(device_name)]['pressure_values'].append(pressure)
            self.regions[(device_name)]['altitude_values'].append(altitude)
            self.regions[(device_name)]['temperature_values'].append(temperature)
    def create_table(self):
        self.update_data()
        # NOT WORKING NOW
        # else:
        #     for idx in range(self.prev_len - 1, self.curr_len -2, -1):
        #         data = self.devices_data[idx]
        #         #print(data)
        #         #print(type(data))
        #         if device_name not in self.device_names:
        #             self.device_names.append(device_name)
        #         device_timestamp = data['device_timestamp']
        #         latitude = float(data['location'][0]['latitude'])
        #         longitude = float(data['location'][1]['longitude'])
        #         pm2_5 = float(data['sensordatavalues'][0]['value'])
        #         pm10 = float(data['sensordatavalues'][1]['value'])
        #         pm_mean = (pm2_5 + pm10) / 2 
        #         for i in range(len(self.pm_2_5_gradation)):
        #             if pm_mean < self.pm_2_5_gradation[i]:
        #                 color = self.pm_gradation_color[i]
        #                 break

        #         if (device_name) not in self.regions:
        #             self.regions[(device_name)] = {'pm2_5_values': [], 'pm10_values': [], 
        #                                                     'color': color, 
        #                                                    'device_timestamp': device_timestamp, 
        #                                                    'latitude' : latitude,
        #                                                    'longitude' : longitude}

        #         self.regions[(device_name)]['pm2_5_values'].append(pm2_5)
        #         self.regions[(device_name)]['pm10_values'].append(pm10)
        self.prev_len = len(self.devices_data)     
        self.selected_device = st.sidebar.selectbox('Выберите аппарат', self.device_names, on_change=self.add_point)
        for idx in range(self.prev_len - 1, 0, -1):
            data = self.devices_data[idx]
            #print(data)
            #print(type(data))
            if self.selected_device == data['device_name']:

                device_timestamp = data['device_timestamp']
                latitude = float(data['location'][0]['latitude'])
                longitude = float(data['location'][1]['longitude'])

                try:
                    pm2_5 = float(data['sensordatavalues'][0]['value'])
                    pm10 = float(data['sensordatavalues'][1]['value'])
                    pressure = float(data['sensordatavalues'][2]['value'])
                    altitude = float(data['sensordatavalues'][3]['value'])
                    temperature = float(data['sensordatavalues'][4]['value'])
                except:
                    pm2_5 = -1
                    pm10 = -1
                    pressure = -1
                    altitude = -1
                    temperature = -1
                break


        
        # Отображение данных выбранного аппарата
        st.sidebar.subheader('Значение аппарата')
        data = {
            'Тип параметра': ['Дата', 'Latitude', 'Longitude', 'Значение PM2_5', 'Значение PM10', 'Давление', 'Высота', 'Температура'],
            'Значение': [device_timestamp,
                        latitude, 
                        longitude, 
                        pm2_5,
                        pm10,
                        pressure,
                        altitude,
                        temperature],
            'Нормальное значение': ['-', '-', '-', self.pm_2_5_gradation[0], self.pm_10_gradation[0] , '-', '-','-']
        }

        st.sidebar.write(pd.DataFrame(data))     


    def create_map(self):
        print('create_map')
        for device, values in self.regions.items():
            # print('--------------------------------')
            # print(device,values)
            # print('--------------------------------')
            latitude = values['latitude']
            longitude = values['longitude']
            # Creating choropleth map with average PM2.5 and PM10 values
            self.map = folium.Map(location=(latitude[0], longitude[0]), zoom_start=7)
            break
    def add_point(self):
        print('add_point')
        self.update_data()
        for feature in self.map._children:
            if isinstance(feature, folium.features.Choropleth):
                self.map._children.pop(feature)
        latitude_set = []
        longitude_set = []
        for devicec, values in self.regions.items():
            #print(values)
            if devicec == self.selected_device:
                for i in range(len(values['latitude'])):

                    latitude = values['latitude'][i]
                    longitude = values['longitude'][i]
                    color = values['color'][i]
                    avg_pm2_5 = values['pm2_5_values'][i]
                    avg_pm10 = values['pm10_values'][i]
                    if (latitude not in latitude_set) and (longitude not in longitude_set):
                        #map = folium.Map(location=[latitude, longitude], zoom_start=7)
                        #print(latitude, longitude)
                        square_coords = [
                            (longitude - 1/111, latitude - 1/111 ),
                            (longitude - 1/111, latitude + 1/111 ),
                            (longitude + 1/111, latitude + 1/111 ),
                            (longitude + 1/111, latitude - 1/111 ),
                            (longitude - 1/111, latitude - 1/111 )
                        ]

                        # Create GeoJSON-like data for the square
                        geo_data = {
                            'type': 'FeatureCollection',
                            'features': [
                                {
                                    'type': 'Feature',
                                    'geometry': {
                                        'type': 'Polygon',
                                        'coordinates': [square_coords]
                                    },
                                    'properties': {
                                        'color': color,
                                        'avg_pm2_5': avg_pm2_5,
                                        'avg_pm10': avg_pm10
                                    }
                                }
                            ]
                        }
                        folium.Choropleth(
                            geo_data=geo_data,
                            name='choropleth',
                            fill_color=color,
                            line_color=color,
                            fill_opacity=0.7,
                            line_opacity=0.2,
                            highlight=True,
                            show=True
                        ).add_to(self.map)

                        # print("VALUES")
                        # print(values)
                        # print("!!!!COLORR")
                        # print(color)
                        folium.Marker(
                            location=[latitude, longitude],
                            icon=folium.Icon(icon_color=color, color=color),
                        ).add_to(self.map)
                        print(f'---->{devicec}')
                    latitude_set.append(latitude)
                    longitude_set.append(longitude)
        st_folium(self.map, width=1000, height=500)
        #print(len(values['latitude']))
    def to_isoformat(self,date_str):
        if "T" in date_str:
            # If the string already contains "T", remove "Z" if present and convert directly
            date_str = date_str.replace("Z", "")
            return datetime.fromisoformat(date_str)
        else:
            # If "T" is not present, add "T" between date and time
            return datetime.fromisoformat(date_str[:10] + 'T' + date_str[10:])
    def sort_by_time(self):
        print('sort by time')
        self.create_map()
        #self.update_data()
        latitude_set = []
        longitude_set = []
        
        for devicec, values in self.regions.items():
            #print(values)
            if devicec == self.selected_device:
                print(values)
                for i in range(len(values['latitude'])):
                    start_date = self.to_isoformat(str(self.start_date) + str(self.start_time))
                    end_date =   self.to_isoformat(str(self.end_date) + str(self.end_time))
                    print(f"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!{self.to_isoformat(values['device_timestamp'][i])} >= {start_date}")
                    print(self.to_isoformat(values['device_timestamp'][i]) >= start_date)
                    if (self.to_isoformat(values['device_timestamp'][i]) <= end_date) and (self.to_isoformat(values['device_timestamp'][i]) >= start_date):    
                        print("OKKKKSKSMDKSMDKSDMKDSMSK")
                        latitude = values['latitude'][i]
                        longitude = values['longitude'][i]
                        color = values['color'][i]
                        avg_pm2_5 = values['pm2_5_values'][i]
                        avg_pm10 = values['pm10_values'][i]
                        if (latitude not in latitude_set) and (longitude not in longitude_set):
                            #map = folium.Map(location=[latitude, longitude], zoom_start=7)
                            print(latitude, longitude)
                            square_coords = [
                                (longitude - 1/111, latitude - 1/111 ),
                                (longitude - 1/111, latitude + 1/111 ),
                                (longitude + 1/111, latitude + 1/111 ),
                                (longitude + 1/111, latitude - 1/111 ),
                                (longitude - 1/111, latitude - 1/111 )
                            ]

                            # Create GeoJSON-like data for the square
                            geo_data = {
                                'type': 'FeatureCollection',
                                'features': [
                                    {
                                        'type': 'Feature',
                                        'geometry': {
                                            'type': 'Polygon',
                                            'coordinates': [square_coords]
                                        },
                                        'properties': {
                                            'color': color,
                                            'avg_pm2_5': avg_pm2_5,
                                            'avg_pm10': avg_pm10
                                        }
                                    }
                                ]
                            }
                            folium.Choropleth(
                                geo_data=geo_data,
                                name='choropleth',
                                fill_color=color,
                                line_color=color,
                                fill_opacity=0.7,
                                line_opacity=0.2,
                                highlight=True,
                                show=True
                            ).add_to(self.map)

                            # print("VALUES")
                            # print(values)
                            # print("!!!!COLORR")
                            # print(color)
                            folium.Marker(
                                location=[latitude, longitude],
                                icon=folium.Icon(icon_color=color, color=color),
                            ).add_to(self.map)
                            print(f'---->{devicec}')
                        latitude_set.append(latitude)
                        longitude_set.append(longitude)
        st_folium(self.map, width=1000, height=500)
        
        
        
        
    # Главная часть приложения
    def main(self):
        st.title('Анализ данных с аппаратов')
        st.markdown(
            """
        <style>
        [data-testid="stSidebar"][aria-expanded="true"]{
            min-width: 30%;
            max-width: 30%;
        }s
        </style>
            """,
            unsafe_allow_html=True,
        )   
        
        # Создаем демонстрационные данные
        data = pd.DataFrame({
            'Datetime': pd.date_range(start='2024-01-01', end='2024-04-30', freq='H'),
        })

        # Заголовок приложения
        st.sidebar.subheader('Анализ временного диапазона')

        # Выводим виджеты для выбора временного диапазона
        # start_date = st.sidebar.date_input("Выберите начальную дату", min_value=data['Date'].min(), max_value=data['Date'].max())
        # end_date = st.sidebar.date_input("Выберите конечную дату", min_value=data['Date'].min(), max_value=data['Date'].max())
        # Выводим виджеты для выбора временного диапазона
        self.start_date = st.sidebar.date_input("Выберите начальную дату", min_value=data['Datetime'].min(), max_value=data['Datetime'].max())
        self.start_time = st.sidebar.time_input('Выберите начальное время', value=None)
        self.end_date = st.sidebar.date_input("Выберите конечную дату и время", min_value=data['Datetime'].min(), max_value=data['Datetime'].max())
        self.end_time = st.sidebar.time_input('Выберите конечное время', value=None)
        # Добавляем кнопку для считывания данных
        st.sidebar.button('Считать временные данные',on_click=self.sort_by_time)
        # Отображение таблицы
        st.sidebar.subheader('Выбор аппарата')
        self.create_table()
        # Отображение карты
        st.subheader('Интерактивная карта')
        self.create_map()
        self.add_point()
        time.sleep(5)
        # Аналитика
        st.subheader('Результат анализа')
        st.write("Зеленый цвет - Норма.")
        st.write("Оранжевый цвет - Чуть выше нормы.")
        st.write("Фиолетовый цвет - Выше нормы.")
        






if __name__ == '__main__':
    global oem
    oem = OEM()
    oem.main()
        # Define a function to call update_data periodically
    def update_periodically():
        while True:
            oem.update_data()
            time.sleep(10)
            print("!!! ON UPDATE")
    # Create a thread for calling update_periodically
    update_thread = threading.Thread(target=update_periodically)

    # Start the thread
    update_thread.start()

    # Keep the main thread running
    while True:
        time.sleep(1)  # This is to prevent the main thread from exiting