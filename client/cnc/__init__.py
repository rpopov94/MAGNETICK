import glob
import logging
import sys
import serial
import serial.tools.list_ports


ports = list(serial.tools.list_ports.comports())

dict_port = {}

for port, desc, hwid in ports:
    dict_port[str(desc[:7])] = port

speeds = ['1200','2400', '4800', '9600', '19200', '38400', '57600', '115200']