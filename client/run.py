import os
import sys
import serial
from dotenv import load_dotenv
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import Qt
from cnc import dict_port, speeds
from cnc.protocol import Protocol

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.CONFIG'))


class CncArduino(QtWidgets.QWidget):
    def __init__ (self):
        super().__init__()
        Form, Base = uic.loadUiType("ui/main.ui")
        self.ui = Form()
        self.ui.setupUi(self)

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
            print(f"Port {dict_port['Arduino']} is open")
        except:
            print(serial.SerialException)
        self.p = Protocol(
            max_x=int(os.environ.get('MAX_X')),
            min_x=int(os.environ.get('MIN_X')),
            max_y=int(os.environ.get('MAX_Y')),
            min_y=int(os.environ.get('MIN_Y')),
            max_z=int(os.environ.get('MAX_Z')),
            min_z=int(os.environ.get('MAX_Z')),
            normalize=int(os.environ.get('NORMALIZE'))
        )
        self.ui.init_p.clicked.connect(self.init_param)

    def keyPressEvent(self, e):
        if self.ser is not None:
            if e.key() == Qt.Key_6:
                self.ser.write(self.p.move_x(1000))
            elif e.key() == Qt.Key_4:
                self.ser.write(self.p.move_x(1000, -1))
            elif e.key() == Qt.Key_8:
                self.ser.write(self.p.move_y(1000))
            elif e.key() == Qt.Key_2:
                self.ser.write(self.p.move_y(1000, -1))
            elif e.key() == Qt.Key_7:
                self.ser.write(self.p.move_z(1000))
            elif e.key() == Qt.Key_9:
                self.ser.write(self.p.move_z(1000, -1))
            elif e.key() == Qt.Key_Escape:
                self.ser.write(self.p.stop())
        else:
            print("You need to connect port!")
            
    def init_param(self):
        self.ser.write(
        self.p.set_speed(
            int(os.environ.get("SPEED"))
        ))
        self.ser.write(
        self.p.set_acceleration(
            int(os.environ.get("ACCELERATION"))
        ))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = CncArduino()
    window.show()
    sys.exit(app.exec_())



