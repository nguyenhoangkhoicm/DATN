import subprocess
import sys

from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QProgressBar
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QTimer
from PyQt5 import QtCore, QtGui


class WelcomeWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Cài đặt kích thước và màu nền cho cửa sổ
        self.resize(800, 400)
        self.setStyleSheet("background-color: #404040")
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        icon = QtGui.QIcon("image/assistant_icon.ico")
        self.setWindowIcon(icon)

        # Logo
        logo = QLabel(self)
        pixmap = QPixmap('image/logo.png')
        pixmap = pixmap.scaledToWidth(200)
        logo.setPixmap(pixmap)

        # Tiêu đề
        title = QLabel("Đồ án tốt nghiệp", self)
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font: bold 40px; color: #0099FF")

        # Tên đề tài
        topic = QLabel(
            "Tên đề tài: Xây dựng trợ lý ảo thông minh trợ giúp sinh viên", self)
        topic.setAlignment(Qt.AlignCenter)
        topic.setStyleSheet("font: 30px; color: white")

        # GVHD và SVTH
        supervisor = QLabel(
            "GVHD: THS.Huỳnh Quang Đức    -    SVTH: Nguyễn Hoàng Khởi", self)
        supervisor.setAlignment(Qt.AlignCenter)
        supervisor.setStyleSheet("font: 20px; color: red")

        # Thanh tiến trình
        progress_bar = QProgressBar(self)
        progress_bar.setValue(0)
        progress_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid grey;
                border-radius: 5px;
                text-align: center;
                color: white;
            }
            QProgressBar::chunk {
                background-color: #0D47A1;
                width: 20px;
            }
        """)

        # Layout
        vbox = QVBoxLayout()
        vbox.addWidget(logo, alignment=Qt.AlignLeft)
        vbox.addWidget(title)
        vbox.addWidget(topic)
        vbox.addWidget(supervisor)
        vbox.addWidget(progress_bar)

        self.setLayout(vbox)

        # Cập nhật giá trị thanh tiến trình
        self.timer = QTimer()
        self.timer.timeout.connect(lambda: self.update_progress(progress_bar))
        self.timer.start(100)

    def update_progress(self, progress_bar):
        value = progress_bar.value() + 1
        progress_bar.setValue(value)

        if value == 100:
            self.timer.stop()
            self.close()
            subprocess.run(['python', 'assistant_main.py'],
                           creationflags=subprocess.CREATE_NO_WINDOW)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = WelcomeWindow()
    window.show()
    sys.exit(app.exec_())
