#-*- coding: utf-8 -*-

import datetime
import csv
from pickle import FALSE
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

def save_data(save_z=False, newline='\n', delimiter='\t\t'):
    f = open(f'{datetime.today().strftime("%d_%m_%y")}.txt', 'w')
    if save_z:
        header = ['x', 'y', 'z', 'Bx', 'By', f'Bz{newline}']
        f.write("\t".join(header))
        f.close()
        with open(f'{datetime.today().strftime("%d_%m_%y")}.txt', 'a', newline=newline) as data:
            for i in range(len(coors_x)):
                data.write(f"{delimiter}".join([
                    str(coors_x[i]), 
                    str(coors_y[i]),
                    str(coors_z[i]),
                    str(res[1][i]),
                    str(res[2][i]),
                    str(res[0][i]), 
                    newline
                ]))
            data.close()          
    else:
        header = ['x', 'y', 'Bx', f'By{newline}']
        f.write("\t".join(header))
        f.close()
        with open(f'{datetime.today().strftime("%d_%m_%y")}.txt', 'a', newline=newline) as data:
            for i in range(len(coors_x)):
                data.write(f"{delimiter}".join(
                    [
                        str(coors_x[i]), 
                        str(coors_y[i]),
                        str(res[1][i]),
                        str(res[2][i]),  
                        newline
                    ]
                ))
            data.close()


def get_data(port):
    return port.readline().decode().split()


def calculate(val):
    return float(val * 600 * 0.0000152587890625)


def get_mas(mass):
    try:
        res[0].append(calculate(int(mass[0]) -23))
        res[1].append(calculate(int(mass[1]) -13))
        res[2].append(calculate(int(mass[2]) -25))
        res[3].append(int(mass[3]))
    except:
        pass
    return res


def get_mean():
    try:
        mag.append((res[0][-1] + res[1][-1] + res[2][-1]) / 3)
    except:
        pass
