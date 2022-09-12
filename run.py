# !/usr/local/bin/python
# -*- coding: utf-8 -*-
import os
import serial
from dotenv import load_dotenv
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import Qt
from client.cnc import dict_port, conf, loadConfig, saveConfig
from client.cnc.protocol import Protocol
from client.magnetron._xyz import XYZ
from client.magnetron._magnetic import Magnetic
from client import save_data, get_data, get_mas, get_mean, save_coors
import sys


basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.config'))

class CncArduino(QtWidgets.QWidget):
    go = int(os.environ.get('N_STEP'))
    def __init__(self):
        super().__init__()
        Form, Base = uic.loadUiType(basedir + "/client/ui/main.ui")
        self.ui = Form()
        self.ui.setupUi(self)
        self.data = None

        self.ser = None
        self.mag_ser = None

        try:
            self.ser = serial.Serial(
                port=dict_port['Arduino'],
                baudrate=int(os.environ.get('BAUDRATE')),
                bytesize=8,
                parity='N',
                stopbits=2,
                timeout=0.1,
                writeTimeout=1,
            )
            self.ui.textBrowser.append(f"Port {dict_port['Arduino']} is open")
        except:
            self.ui.textBrowser.append(f"Arduino port not connected.")

        try:
            self.mag_ser = serial.Serial(
                port=os.environ.get('3DMAG_SER'),
                baudrate=9600,
                bytesize=8,
                parity='N',
                stopbits=2,
                timeout=0.1,
                writeTimeout=1,
            )
        except:
            self.ui.textBrowser.append(f"Holl sensor not connected.")

        if not os.path.exists("coords.json"):
            self.data = conf
        else:
            self.data = loadConfig("coords.json")

        self.pos_x = int(self.data['current_x'])
        self.pos_y = int(self.data['current_y'])
        self.pos_z = int(self.data['current_z'])

        self.p = Protocol(
            current_x=int(self.data['current_x']),
            current_y=int(self.data['current_y']),
            current_z=int(self.data['current_y']),
            max_x=int(os.environ.get('MAX_X')),
            min_x=int(os.environ.get('MIN_X')),
            max_y=int(os.environ.get('MAX_Y')),
            min_y=int(os.environ.get('MIN_Y')),
            max_z=int(os.environ.get('MAX_Z')),
            min_z=int(os.environ.get('MIN_Z')),
            normalize=int(os.environ.get('NORMALIZE'))
        )

        self.save_z = int(os.environ.get("SAVE_Z"))

        self.ui.init_p.clicked.connect(self.init_param)
        self.ui.clear_b.clicked.connect(self.clear_w)
        self.ui.stop_b.clicked.connect(self.stop_m)
        self.ui.x_right.clicked.connect(self.rx_)
        self.ui.x_left.clicked.connect(self.lx_)
        self.ui.y_right.clicked.connect(self.ry_)
        self.ui.y_left.clicked.connect(self.ly_)
        self.ui.z_right.clicked.connect(self.rz_)
        self.ui.z_left.clicked.connect(self.lz_)
        self.ui.real_st_b.clicked.connect(self.setmax_r)
        self.ui.end_real_b.clicked.connect(self.setmin_r)
        self.ui.teor_st_b.clicked.connect(self.setmax_t)
        self.ui.end_teor_b.clicked.connect(self.setmin_t)

        self.x_w = XYZ('RAW_X', component=1)
        self.y_w = XYZ('RAW_Y', component=2)
        self.z_w = XYZ('RAW_Z', component=0)
        self.m_w = Magnetic()

        self.ui.z_raw.clicked.connect(self.graph_z)
        self.ui.x_raw.clicked.connect(self.graph_x)
        self.ui.y_raw.clicked.connect(self.graph_y)
        self.ui.mean_raw.clicked.connect(self.graph_m)

    def graph_z(self):
        self.z_w.show()

    def graph_x(self):
        self.x_w.show()

    def graph_y(self):
        self.y_w.show()

    def graph_m(self):
        self.m_w.show()

    def setmax_r(self):
        self.ser.write(self.p.gotomax())
        self.ui.textBrowser.append(f"coordinats : in real end position")

    def setmin_r(self):
        self.ser.write(self.p.gotomin())
        self.ui.textBrowser.append(f"coordinats : in real start position")

    def setmax_t(self):
        self.ser.write(self.p.go_to_x(current=self.pos_x))
        self.ser.write(self.p.go_to_y(current=self.pos_y))
        self.ser.write(self.p.go_to_z(current=self.pos_z))
        self.ui.textBrowser.append(f"coordinats : in set end position")

    def setmin_t(self):
        self.ser.write(self.p.go_to_x(current=self.pos_x, dir=-1))
        self.ser.write(self.p.go_to_y(current=self.pos_y, dir=-1))
        self.ser.write(self.p.go_to_z(current=self.pos_z, dir=-1))
        self.ui.textBrowser.append(f"coordinats : in set start position")

    def rx_(self):
        save_coors([self.pos_x, self.pos_y, self.pos_z])
        if self.pos_x < self.p.max_x:
            self.pos_x += self.go
            self.ser.write(self.p.move_x(self.go))
        get_mas(get_data(self.mag_ser))
        self.ui.textBrowser.append(f"pos_x :{self.pos_x}, pos_y :{self.pos_y}, pos_z :{self.pos_z}")
        
    def lx_(self):
        save_coors([self.pos_x, self.pos_y, self.pos_z])
        if self.p.min_x < self.pos_x:
            self.pos_x -= self.go
            self.ser.write(self.p.move_x(self.go, dir=-1))
        get_mas(get_data(self.mag_ser))
        self.ui.textBrowser.append(f"pos_x :{self.pos_x}, pos_y :{self.pos_y}, pos_z :{self.pos_z}")

    def ry_(self):
        save_coors([self.pos_x, self.pos_y, self.pos_z])
        if self.pos_y < self.p.max_y:
            self.pos_y += self.go
            self.ser.write(self.p.move_y(self.go, dir=-1))
        get_mas(get_data(self.mag_ser))
        self.ui.textBrowser.append(f"pos_x :{self.pos_x}, pos_y :{self.pos_y}, pos_z :{self.pos_z}")
        
    def ly_(self):
        save_coors([self.pos_x, self.pos_y, self.pos_z])
        if self.p.min_y < self.pos_y:
            self.pos_y -= self.go
            self.ser.write(self.p.move_y(self.go))
        get_mas(get_data(self.mag_ser))
        self.ui.textBrowser.append(f"pos_x :{self.pos_x}, pos_y :{self.pos_y}, pos_z :{self.pos_z}")

    def rz_(self):
        save_coors([self.pos_x, self.pos_y, self.pos_z])
        if self.pos_z < self.p.max_z:
            self.pos_z += self.go
            self.ser.write(self.p.move_z(self.go))
        get_mas(get_data(self.mag_ser))
        self.ui.textBrowser.append(f"pos_x :{self.pos_x}, pos_y :{self.pos_y}, pos_z :{self.pos_z}")
        
    def lz_(self):
        save_coors([self.pos_x, self.pos_y, self.pos_z])
        if self.p.min_z < self.pos_z:
            self.pos_z -= self.go
            self.ser.write(self.p.move_z(self.go, dir=-1))
        get_mas(get_data(self.mag_ser))
        self.ui.textBrowser.append(f"pos_x :{self.pos_x}, pos_y :{self.pos_y}, pos_z :{self.pos_z}")

    def keyPressEvent(self, e):
        get_mas(get_data(self.mag_ser))
        get_mean()
        if self.ser is not None:
            if e.key() == Qt.Key_4:
                if int(self.p.min_x[0]) < self.pos_x:
                    self.pos_x -= self.go
                    self.ser.write(self.p.move_x(self.go))
                self.ui.textBrowser.append(f"pos_x :{self.pos_x}, pos_y :{self.pos_y}, pos_z :{self.pos_z}")
            elif e.key() == Qt.Key_6:
                if self.pos_x < int(self.p.max_x[0]):
                    self.pos_x += self.go
                    self.ser.write(self.p.move_x(self.go, -1))
                self.ui.textBrowser.append(f"pos_x :{self.pos_x}, pos_н :{self.pos_y}, pos_z :{self.pos_z}")
            elif e.key() == Qt.Key_8:
                if self.pos_y < int(self.p.max_y[0]):
                    self.pos_y += self.go
                    self.ser.write(self.p.move_y(self.go, -1))
                self.ui.textBrowser.append(f"pos_x :{self.pos_x}, pos_y :{self.pos_y}, pos_z :{self.pos_z}")
            elif e.key() == Qt.Key_2:
                if self.pos_y < int(self.p.max_y[0]):
                    self.pos_y -= self.go
                    self.ser.write(self.p.move_y(self.go))
                self.ui.textBrowser.append(f"pos_x :{self.pos_x}, pos_y :{self.pos_y}, pos_z :{self.pos_z}")
            elif e.key() == Qt.Key_7:
                if self.pos_z < int(self.p.max_z[0]):
                    self.pos_z -= self.go
                    self.ser.write(self.p.move_z(self.go, -1))
                self.ui.textBrowser.append(f"pos_x :{self.pos_x}, pos_y :{self.pos_y}, pos_z :{self.pos_z}")
            elif e.key() == Qt.Key_9:
                if int(self.p.min_z[0]) < self.pos_z:
                    self.pos_z += self.go
                    self.ser.write(self.p.move_z(self.go))
                self.ui.textBrowser.append(f"pos_x :{self.pos_x}, pos_y :{self.pos_y}, pos_z :{self.pos_z}")
            elif e.key() == Qt.Key_1:
                self.setmax_r()
            elif e.key() == Qt.Key_3:
                self.setmin_r()
            elif e.key() == Qt.Key_Plus:
                self.setmax_t()
            elif e.key() == Qt.Key_Minus:
                self.setmin_t()
            elif e.key() == Qt.Key_Escape:
                self.ser.write(self.p.stop())
            save_coors([self.pos_x, self.pos_y, self.pos_z])
        else:
            self.ui.textBrowser.append("You need to connect port!")

    def closeEvent(self, e):
        result = QtWidgets.QMessageBox.question(self,
            "Подтверждение закрытия окна",
            "Сохранить результаты измерения?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
            QtWidgets.QMessageBox.No)
        if result == QtWidgets.QMessageBox.Yes:
            e.accept()
            self.p.stop()
            save_data(self.save_z)
            saveConfig({"current_x": self.pos_x, "current_y": self.pos_y, "current_z": self.pos_z}, "coords.json")
            QtWidgets.QWidget.closeEvent(self, e)
        else:
            saveConfig({"current_x": self.pos_x, "current_y": self.pos_y, "current_z": self.pos_z}, "coords.json")
            QtWidgets.QWidget.closeEvent(self, e)

    def init_param(self):
        self.ser.write(
            self.p.set_speed(
                int(os.environ.get("SPEED"))
            ))
        self.ser.write(
            self.p.set_acceleration(
                int(os.environ.get("ACCELERATION"))
            ))
        self.ui.textBrowser.append(f"Скорость: {os.environ.get('SPEED')}\nУскорение: {os.environ.get('ACCELERATION')}")

    def clear_w(self):
        self.ui.textBrowser.clear()

    def stop_m(self):
        self.ser.write(self.p.stop())


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = CncArduino()
    window.show()
    sys.exit(app.exec_())
