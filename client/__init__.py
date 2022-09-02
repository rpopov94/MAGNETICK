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
    if save_z:
       np.savetxt(f'{datetime.today().strftime("%d_%m_%y")}.txt',
            np.array([coors_x, coors_y, coors_z,  res[1], res[2], res[0]]),
            fmt='%.18e',
            delimiter='\t\t',
            newline='\n',
            header="x	y	Bx	By",
            comments=''
        )
    else: 
        np.savetxt(f'{datetime.today().strftime("%d_%m_%y")}.txt',
            np.array([coors_x, coors_y, res[0], res[1]]),
            fmt='%.18e',
            delimiter='\t\t',
            newline='\n',
            header="x	y	Bx	By",
            comments=''
        )


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
