import datetime
import numpy as np
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


def save_data(save_z=False):
    f = open(f'{datetime.today().strftime("%d_%m_%y")}.txt', 'w')
    f.close()
    import csv
    with open(f'{datetime.today().strftime("%d_%m_%y")}.txt', 'w',  encoding='UTF8', newline='') as save_data:
        if save_z:
            header = ['x', 'y', 'z', 'Bx', 'By', 'Bz']
            rows =  {'x': coors_x, 'y': coors_y, 'z': coors_z, 'Bx': res[1], 'By': res[2], 'Bz': res[2]}
            write = csv.DictWriter(save_data, fieldnames=header)
            write.writeheader()
            write.writerows(rows)
        else:
            header = ['x', 'y', 'Bx', 'By']
            rows =  {'x': coors_x, 'y': coors_y, 'Bx': res[1], 'By': res[2]}
            write = csv.DictWriter(save_data, fieldnames=header)
            write.writeheader()
            write.writerows(rows)
        save_data.close()





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
