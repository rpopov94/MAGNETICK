import json
import serial.tools.list_ports

ports = list(serial.tools.list_ports.comports())

conf = {"current_x": 0, "current_y": 0, "current_z": 0}

dict_port = {}

for port, desc, hwid in ports:
    dict_port[str(desc[:7])] = port

speeds = ['1200', '2400', '4800', '9600', '19200', '38400', '57600', '115200']


def saveConfig(dictionary, File):
    with open(File, "w") as myFile:
        json.dump(dictionary, myFile)
        myFile.close()


def loadConfig(File):
    with open(File, "r") as myFile:
        dict = json.load(myFile)
        myFile.close()
    return dict
