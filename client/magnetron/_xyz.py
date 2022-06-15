from PyQt5 import QtCore
from PyQt5.QtWidgets import QDialog, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
from client import res


class MonitorPort(QtCore.QObject):
    signal_x = QtCore.pyqtSignal(list)

    def __int__(self):
        super().__init__()

    def run(self):
        while True:
            self.signal_x.emit(res)
            QtCore.QThread.msleep(1000)


class XYZ(QDialog):
    def __init__(self, gname, component, parent=None):
        super(XYZ, self).__init__(parent)

        self.component = component
        self.setWindowTitle(gname)
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)

        layout = QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)

        self.setLayout(layout)

        self.two_thread = QtCore.QThread()
        self.browserHandler = MonitorPort()
        self.browserHandler.moveToThread(self.two_thread)
        self.browserHandler.signal_x.connect(self.plot)
        self.two_thread.started.connect(self.browserHandler.run)
        self.two_thread.start(QtCore.QThread.LowestPriority)

    @QtCore.pyqtSlot(list)
    def plot(self, data):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.grid(True)
        ax.plot(data[self.component], '*-')
        self.canvas.draw()
