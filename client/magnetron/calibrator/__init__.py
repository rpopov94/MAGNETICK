from PyQt5 import QtCore


class Calibrator(QtCore.QObject):
    an_slot = QtCore.pyqtSignal()

    def __int__(self):
        super().__init__()

    def run(self):
        while True:
            self.an_slot.emit()
            QtCore.QThread.msleep(100)