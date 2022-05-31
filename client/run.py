import os
import json
import serial
from dotenv import load_dotenv
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import Qt
from cnc import dict_port, conf, loadConfig
from cnc.protocol import Protocol

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.CONFIG'))


class CncArduino(QtWidgets.QWidget):

    with_st = int(os.environ.get('N_STEP'))
    normalize = int(os.environ.get('NORMALIZE'))
    go = with_st * normalize
    
    def __init__ (self):
        super().__init__()
        Form, Base = uic.loadUiType(basedir + "/ui/main.ui")
        self.ui = Form()
        self.ui.setupUi(self)
        self.data = None

        self.ser = None
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
            self.ui.textBrowser.append(f"Arduino port not connected")

        if not os.path.exists("coords.json"):
            f = open("coords.json", 'w')
            json.dump(conf, f)
            f.close()
        else:
            self.data = loadConfig("coords.json")

        self.pos_x = int(self.data['current_x'])
        self.pos_y = int(self.data['current_y'])
        self.pos_z = int(self.data['current_z'])

        self.p = Protocol(
            current_x = int(self.data['current_x']),
            current_y = int(self.data['current_y']),
            current_z = int(self.data['current_y']),
            max_x = int(os.environ.get('MAX_X')),
            min_x = int(os.environ.get('MIN_X')),
            max_y = int(os.environ.get('MAX_Y')),
            min_y = int(os.environ.get('MIN_Y')),
            max_z = int(os.environ.get('MAX_Z')),
            min_z = int(os.environ.get('MAX_Z')),
            normalize = int(os.environ.get('NORMALIZE'))
        )

        self.ui.init_p.clicked.connect(self.init_param)
        self.ui.clear_b.clicked.connect(self.clear_w)
        self.ui.stop_b.clicked.connect(self.stop_m)
        self.ui.x_right.clicked.connect(self.rx_)
        self.ui.x_left.clicked.connect(self.lx_)
        self.ui.y_right.clicked.connect(self.ry_)
        self.ui.y_left.clicked.connect(self.ly_)
        self.ui.z_right.clicked.connect(self.rz_)
        self.ui.z_left.clicked.connect(self.lz_)
        self.ui.set_max_x.clicked.connect(self.setmax_x)
        self.ui.set_max_y.clicked.connect(self.setmax_y)
        self.ui.set_max_z.clicked.connect(self.setmax_z)
        self.ui.set_min_x.clicked.connect(self.setmin_x)
        self.ui.set_min_y.clicked.connect(self.setmin_y)
        self.ui.set_min_z.clicked.connect(self.setmin_z)

    def setmax_x(self):
        self.ser.write(self.p.go_to_x(int(os.environ.get('MAX_X'))))

    def setmax_y(self):
        self.ser.write(self.p.go_to_y(int(os.environ.get('MAX_Y'))))

    def setmax_z(self):
        self.ser.write(self.p.go_to_z(int(os.environ.get('MAX_Z'))))

    def setmin_x(self):
        self.ser.write(self.p.go_to_x(int(os.environ.get('MIN_X'))))

    def setmin_y(self):
        self.ser.write(self.p.go_to_y(int(os.environ.get('MIN_Y'))))

    def setmin_z(self):
        self.ser.write(self.p.go_to_z(int(os.environ.get('MIN_Z'))))

    def rx_(self):
        self.pos_x += self.with_st
        self.ser.write(self.p.move_x(self.go))
        self.ui.textBrowser.append(f"pos_x :{self.pos_x}")
        conf['current_x'] = self.pos_x

    def lx_(self):
        self.pos_x -= self.with_st
        self.ser.write(self.p.move_x(self.go, -1))
        self.ui.textBrowser.append(f"pos_x :{self.pos_x}")
        conf['current_x'] = self.pos_x

    def ry_(self):
        self.pos_y += self.with_st
        self.ser.write(self.p.move_y(self.go))
        self.ui.textBrowser.append(f"pos_y :{self.pos_y}")
        conf['current_y'] = self.pos_y

    def ly_(self):
        self.pos_y -= self.with_st
        self.ser.write(self.p.move_y(self.go, -1))
        self.ui.textBrowser.append(f"pos_y :{self.pos_y}")
        conf['current_y'] = self.pos_y

    def rz_(self):
        self.pos_z -= self.with_st
        self.ser.write(self.p.move_z(self.go))
        self.ui.textBrowser.append(f"pos_z :{self.pos_z}")
        conf['current_z'] = self.pos_z

    def lz_(self):
        self.pos_z -= self.with_st
        self.ser.write(self.p.move_z(self.go, -1))
        self.ui.textBrowser.append(f"pos_z :{self.pos_z}")
        conf['current_z'] = self.pos_z

    def keyPressEvent(self, e):
        if self.ser is not None:
            if e.key() == Qt.Key_6:
                self.pos_x += self.with_st
                self.ser.write(self.p.move_x(self.go))
                self.ui.textBrowser.append(f"pos_x :{self.pos_x}")
            elif e.key() == Qt.Key_4:
                self.pos_x -= self.with_st
                self.ser.write(self.p.move_x(self.go, -1))
                self.ui.textBrowser.append(f"pos_x :{self.pos_x}")
            elif e.key() == Qt.Key_8:
                self.pos_y += self.with_st
                self.ser.write(self.p.move_y(self.go))
                self.ui.textBrowser.append(f"pos_y :{self.pos_y}")
            elif e.key() == Qt.Key_2:
                self.pos_y -= self.with_st
                self.ser.write(self.p.move_y(self.go, -1))
                self.ui.textBrowser.append(f"pos_y :{self.pos_y}")
            elif e.key() == Qt.Key_7:
                self.pos_z -= self.with_st
                self.ser.write(self.p.move_z(self.go))
                self.ui.textBrowser.append(f"pos_z :{self.pos_z}")
            elif e.key() == Qt.Key_9:
                self.pos_z -= self.with_st
                self.ser.write(self.p.move_z(self.go, -1))
                self.ui.textBrowser.append(f"pos_z :{self.pos_z}")
            elif e.key() == Qt.Key_Escape:
                self.ser.write(self.p.stop())
            conf['current_x'] = self.pos_x
            conf['current_y'] = self.pos_y
            conf['current_z'] = self.pos_z
        else:
            self.ui.textBrowser.append("You need to connect port!")

    def closeEvent(self, e):
        result = QtWidgets.QMessageBox.question(self,
        "Подтверждение закрытия окна",
        "Вы действительно хотите закрыть окно?",
        QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
        QtWidgets.QMessageBox.No)
        if result == QtWidgets.QMessageBox.Yes:
            e.accept()
            self.p.save_param(self.pos_x, self.pos_y, self.pos_z)
            self.p.stop()
            QtWidgets.QWidget.closeEvent(self, e)
        else:
            e.ignore()

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
