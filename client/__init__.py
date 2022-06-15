import datetime
import pandas as pd
from datetime import datetime

res = [[], [], [], []]


def save_data():
    df = pd.DataFrame({
        'z': res[0],
        'x': res[1],
        'y': res[2],
        't': res[3]
    })
    with pd.ExcelWriter(f'{datetime.today().strftime("%y_%m_%d")}.xlsx') as writer:
        df.to_excel(writer, sheet_name='Sheet_name_1', index=False)
    writer.save()
    writer.close()


def get_data(port):
    return port.readline().decode().split()


def calculate(val):
    return float(val * 600 * 0.0000152587890625)


def get_mas(mass):
    res[0].append(int(mass[0]))
    res[1].append(int(mass[1]))
    res[2].append(int(mass[2]))
    res[3].append(int(mass[3]))
    return res
