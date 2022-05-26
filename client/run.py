import sys
from PyQt5 import QtWidgets, uic
from cnc import get_serial_ports, speeds


class ChMLogger(QtWidgets.QWidget):
    def __init__ (self, parent=None):
        super().__init__(parent)
        Form, Base = uic.loadUiType("ui/main.ui")
        self.ui = Form()
        self.ui.setupUi(self)

        self.ui.port.addItems(get_serial_ports())
        self.ui.baudrate.addItems(speeds)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = ChMLogger()
    window.show()
    sys.exit(app.exec_())



