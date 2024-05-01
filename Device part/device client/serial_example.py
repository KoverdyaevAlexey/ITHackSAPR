import serial
import json
 
# ser = 
 
# print('serial test start ...')
# ser.write("Hello Wrold !!!\n")
def get_line():
    with serial.Serial("/dev/ttyUSB0",9600) as ser:
        S = ''
        a = ' '
        while a!='\n':
            a = ser.read().decode()
            if a != '\n':
                S += a
    return S
def get_json():
    data = get_line().replace("'",'"')
    print(data)
    try:
        data = json.loads(data)
        for key in data:
            # if type(data[key]) != str:
            data[key] = str(data[key])
        return data
    except Exception as e:
        print(e)
        return None
# Flush
def flush():
    get_line()
# print(get_line())
# flush()
# print(get_json())