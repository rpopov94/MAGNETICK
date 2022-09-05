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


# def save_data(save_z=False):
#     f = open(f'{datetime.today().strftime("%d_%m_%y")}.txt', 'w')
#     writer = csv.writer(f, delimiter ="\t")
#     if save_z:
#         header = ['x', 'y', 'z', 'Bx', 'By', 'Bz']
#         writer.writerow(header)
#         f.close()
#         with open(f'{datetime.today().strftime("%d_%m_%y")}.txt', 'a', newline='\n') as data:
#             writer_rows = csv.writer(data, delimiter = '\t')
#             for i in range(len(coors_x)):
#                 writer_rows.writerow({
#                     coors_x[i], 
#                     coors_y[i],
#                     coors_z[i],
#                     res[1][i],
#                     res[2][i],
#                     res[0][i]
#                 })
#             data.close()          
#     else:
#         header = ['x', 'y', 'Bx', 'By']
#         writer.writerow(header)
#         f.close()
#         with open(f'{datetime.today().strftime("%d_%m_%y")}.txt', 'a', newline='\n') as data:
#             writer_rows = csv.writer(data, delimiter ="\t")
#             for i in range(len(coors_x)):
#                 writer_rows.writerow({
#                     coors_x[i], 
#                     coors_y[i],
#                     res[1][i],
#                     res[2][i],
#                 })
#             data.close()
def save_data(save_z=False):
    f = open(f'{datetime.today().strftime("%d_%m_%y")}.txt', 'w')
    if save_z:
        header = ['x', 'y', 'z', 'Bx', 'By', 'Bz\n']
        f.write("\t".join(header))
        f.close()
        with open(f'{datetime.today().strftime("%d_%m_%y")}.txt', 'a', newline='\n') as data:
            for i in range(len(coors_x)):
                data.write("\t\t".join([
                    str(coors_x[i]), 
                    str(coors_y[i]),
                    str(coors_z[i]),
                    str(res[1][i]),
                    str(res[2][i]),
                    str(res[0][i]), 
                    '\n'
                ]))
            data.close()          
    else:
        header = ['x', 'y', 'Bx', 'By\n']
        f.write("\t".join(header))
        f.close()
        with open(f'{datetime.today().strftime("%d_%m_%y")}.txt', 'a', newline='\n') as data:
            for i in range(len(coors_x)):
                data.write("\t\t".join(
                    [
                        str(coors_x[i]), 
                        str(coors_y[i]),
                        str(res[1][i]),
                        str(res[2][i]),  
                        '\n'
                    ]
                ))
            data.close()


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
