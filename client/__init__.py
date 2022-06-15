import datetime
import pandas as pd
from datetime import datetime

res = [[], [], [], []]
mag = []

coors_z = []
coors_x = []
coors_y = []


def save_coors(coors):
    coors_z.append(coors[0])
    coors_x.append(coors[1])
    coors_y.append(coors[2])


def save_data():
    df = pd.DataFrame({
        'row_z': res[0],
        'row_x': res[1],
        'row_y': res[2],
        'x': coors_x,
        'y': coors_y,
        'z': coors_z,
        'temperature': res[3]
    })
    with pd.ExcelWriter(f'{datetime.today().strftime("%d_%m_%y")}.xlsx') as writer:
        df.to_excel(writer, sheet_name='sample', index=False)
    writer.save()
    writer.close()


def get_data(port):
    return port.readline().decode().split()


def calculate(val):
    return float(val * 600 * 0.0000152587890625)


def get_mas(mass):
    res[0].append(calculate(int(mass[0]) -23))
    res[1].append(calculate(int(mass[1]) -13))
    res[2].append(calculate(int(mass[2]) -25))
    res[3].append(int(mass[3]))
    return res


def get_mean():
    mag.append((res[0][-1] + res[1][-1] + res[2][-1]) / 3)


def ser_is_open(argument):
    def decorator(function):
        def wrapper(*args, **kwargs):
            if argument is not None:
                return function(*args, **kwargs)
            print("Port not connected")
        return wrapper
    return decorator
