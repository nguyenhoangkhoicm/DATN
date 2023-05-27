from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtGui import QMovie

import sys
import subprocess
import os


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(700, 700)

        MainWindow.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        MainWindow.setAttribute(QtCore.Qt.WA_TranslucentBackground)
       
        icon = QtGui.QIcon("image/assistant_icon.ico")
        MainWindow.setWindowIcon(icon)

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.updateGif)
        self.timer.start(1000)

        # center main window on screen
        desktop = QtWidgets.QApplication.desktop()
        screen_rect = desktop.screenGeometry()
        x = (screen_rect.width() - MainWindow.width()) / 2
        y = (screen_rect.height() - MainWindow.height()) / 2
        MainWindow.move(x, y)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # create label
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setMinimumSize(QtCore.QSize(566, 566))
        self.label.setMaximumSize(QtCore.QSize(566, 566))
        self.label.setObjectName("label")

        x = (MainWindow.width() - self.label.width()) / 2
        y = (MainWindow.height() - self.label.height()) / 2
        self.label.move(x, y)

        # add label to main window
        MainWindow.setCentralWidget(self.centralwidget)

    def updateGif(self):
        if os.path.exists('voice.mp3'):
            self.movie = QMovie("image/rob.gif")
            self.label.setMovie(self.movie)
            self.movie.start()
            animation = QtCore.QPropertyAnimation(self.label, b'geometry')
            animation.setDuration(1000)
            animation.setStartValue(self.label.geometry())
            animation.setEndValue(self.label.geometry().translated(100, 100))
            animation.start()
        else:
            self.label.clear()

    def run_task(self):

        self.thread = QtCore.QThread()
        self.worker = Worker()
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.start()


class Worker(QtCore.QObject):
    finished = QtCore.pyqtSignal()

    def run(self):
        subprocess.Popen(['python', 'main.py'],
                         creationflags=subprocess.CREATE_NO_WINDOW)
        self.finished.emit()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(window)
    ui.run_task()
    window.show()
    sys.exit(app.exec_())
