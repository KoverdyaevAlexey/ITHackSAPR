#include <Arduino.h>
#include <TroykaIMU.h>
#include <DHT11.h>
#include <SDS011.h>


// int temperature_max = 100;
// int temperature_min = 100;

// int humidity_max = 100;
// int humidity_min = 0;
// int humidity = {0,0,0,0,0,0,0,0};

void setup()
{
  // открываем последовательный порт
  Serial.begin(9600);
  barometer_setup();
  pm_setup();
}

// ------------------------ LIGHT ------------------------
// библиотека для работы с датчиком освещённости (Troyka-модуль)
// #include <TroykaLight.h>

// создаём объект для работы с датчиком освещённости
// и передаём ему номер пина выходного сигнала
// TroykaLight sensorLight(26);
#define LIGHT_PIN 26
// resistance other resistor for divider (Ohm)
#define RES_DIVIDER         10000.0
#define MULT_VALUE          32017200.0
#define POW_VALUE           1.5832
#define LUX_TO_FOOT_CANDLES 10.764

#define SAMPLE_TIMES        32
#define ADC_BIT             12
#define ADC_VALUE_MAX       pow(2, ADC_BIT)

float light_read_lux(int _pin) {
    int sensorADC = 0;
    float sensorRatio = 0;
    float sensorResistance = 0;
    for (int i = 0; i < SAMPLE_TIMES; i++) {
        sensorADC += analogRead(_pin);
    }
    // Serial.printf("%f\n", sensorADC);
    sensorADC = sensorADC >> 5;
    sensorRatio = (float)ADC_VALUE_MAX / (float)sensorADC - 1.0;
    // Serial.printf("%f %f %f\n", ADC_VALUE_MAX, sensorADC, sensorRatio);
    sensorResistance  = RES_DIVIDER / sensorRatio;
    // Serial.printf("%f %f %f\n",MULT_VALUE, sensorResistance, POW_VALUE);
    return MULT_VALUE / (float)pow(sensorResistance, POW_VALUE);
}

float light_read_candle(int _pin) {
  return light_read_lux(_pin) / LUX_TO_FOOT_CANDLES;
}

void publish_light_data() {
  float data = light_read_candle(LIGHT_PIN);
  if (isinf(data)){
    Serial.printf("'light_candle':Infinity"
    );
    return;
  }
  Serial.printf("'light_candle':%f",
    data
  );
}
// ------------------------ LIGHT END ------------------------


// ------------------------ BAROMETER ------------------------
Barometer barometer;
void barometer_setup() {
  barometer.begin();
}
void publish_barometer_data(){
    // Создаём переменную для значения атмосферного давления в Паскалях
    float pressurePascals = barometer.readPressurePascals();
    // Создаём переменную для значения атмосферного давления в мм рт.ст.
    float pressureMillimetersHg = barometer.readPressureMillimetersHg();
    // Создаём переменную для значения высоты над уровнем море
    float altitude = barometer.readAltitude();
    // Создаём переменную для значения температуры окружающей среды
    float temperature = barometer.readTemperatureC();

    // Вывод данных в Serial-порт
    Serial.printf("'pressure_pa':% 6.2f,'altitude_m':% 6.2f,'temperature_c':% 6.2f",
      pressurePascals,
      altitude,
      temperature
    );
}
// ------------------------ BAROMETER END ------------------------

// ------------------------ HUMIDITY ------------------------
DHT11 dht11(27);

void publish_humidity_data() {
    int temperature = 0;
    int humidity = 0;

    // Attempt to read the temperature and humidity values from the DHT11 sensor.
    int result = 1;
    while (result!=0) {
        result = dht11.readTemperatureHumidity(temperature, humidity);
        // Serial.println(DHT11::getErrorString(result));
    }

    // Check the results of the readings.
    // If the reading is successful, print the temperature and humidity values.
    // If there are errors, print the appropriate error messages.
    Serial.printf("'humidity_percent':%d",
      humidity
    );
    // Serial.print("Temperature: ");
    // Serial.print(temperature);
    // Serial.print(" °C\tHumidity: ");
    // Serial.print(humidity);
    // Serial.println(" %");
}
// ------------------------ HUMIDITY END ------------------------


// ------------------------ PM ------------------------
GuL::SDS011 sds(Serial2);

#define RX2 16
#define TX2 17

void pm_setup() {
  Serial2.begin(9600, SERIAL_8N1, RX2, TX2);
  sds.setToPassiveReporting();
}

void publish_pm_data() {
  sds.poll();
  delay(20);
  sds.read();

  // outputFormat.c_str()
  Serial.printf("'PM2.5':% 6.2f, 'PM10':% 6.2f",
                sds.getPM2_5(),
                sds.getPM10());
}

// ------------------------ PM END ------------------------




void loop()
{
  // считывание данных с датчика освещённости
  // sensorLight.read();
  // вывод показателей сенсора освещённости в люксахи
  // Serial.print("Light is ");
  // Serial.print(light_read_lux(LIGHT_PIN));
  // Serial.print(" Lx\n");
  // вывод показателей сенсора освещённости в фут-свечах
  // Serial.print(sensorLight.getLightFootCandles());
  // Serial.println(" Foot Candles");
  // Serial.println("WE STARTED");
  Serial.print("{");
  publish_light_data();
  Serial.print(",");
  publish_barometer_data();
  Serial.print(",");
  publish_humidity_data();
  Serial.print(",");
  publish_pm_data();
  Serial.print("}");
  Serial.print("\n");
  delay(300);
}
