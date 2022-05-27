import sys
import serial
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import Qt
from cnc import get_serial_ports, speeds
from cnc.protocol import Protocol


class ChMLogger(QtWidgets.QWidget):
    def __init__ (self):
        super().__init__()
        Form, Base = uic.loadUiType("ui/main.ui")
        self.ui = Form()
        self.ui.setupUi(self)

        self.ser = None
        self.p = Protocol()
        self.ui.port.addItems(get_serial_ports())
        self.ui.baudrate.addItems(speeds)
        self.ui.connect_port.clicked.connect(self.connect_to_port)

    def connect_to_port(self):
        name = self.ui.port.currentText()
        try:
            self.ser = serial.Serial(
                port=name.upper(),
                baudrate=self.ui.baudrate.currentText(),
                bytesize=8,
                parity='N',
                stopbits=2,
                timeout=0.1,
                writeTimeout=1,
            )
            print(f'Port {name} is open')
        except:
            print(serial.SerialException)

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


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = ChMLogger()
    window.show()
    sys.exit(app.exec_())



