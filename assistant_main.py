
from ai_function.access_schedule import schedule
from ai_function.speaklisten import speaker
from ai_function.point_lookup import point_lookup
from ai_function.sleep import function
from ai_function.determine_most_similar import determine_most_similar_phrase
from intentclassification.intent_classification import IntentClassifier

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QMovie

from googleapiclient.discovery import build

import pyaudio
import json
import random
import sys
import os
import struct
import pvporcupine
import webbrowser
import playsound
import speech_recognition as sr


class AssistantThread(QtCore.QThread):

    answer_signal = QtCore.pyqtSignal(str)

    def __init__(self, name):
        super().__init__()
        self.name = name
        self.intentclassifier = IntentClassifier()

    def command(self, count=0):
        playsound.playsound("./sound/Ping.mp3", False)
        r = sr.Recognizer()
        with sr.Microphone() as source:
            audio = r.record(source, duration=6)
            try:
                text = r.recognize_google(audio, language='vi')
                print("🧑: " + text)
                if text.lower() == "hey siri":
                    count = 0
            except sr.UnknownValueError:

                text = "Xin lỗi tôi không nghe thấy bạn nói gì, bạn có thể nói lại không."
                self.answer_signal.emit(text)
                speaker.speak(text)
                count += 1

                if count == 3:

                    text = "Tôi sẽ tạm dừng cho đến khi bạn gọi tên Hey siri"

                    speaker.speak(text)

                    while True:
                        try:
                            speaker.siri()
                            break
                        except sr.UnknownValueError:
                            pass
                    count = 0

                text = speaker.command(count)

        return text.lower()

    def run(self):
        with open('samples/hello_assistant.json', encoding='utf-8') as f:
            data = json.load(f)
            self.questions = data.get('', [])
        question = random.choice(self.questions)
        self.answer_signal.emit(question)
        speaker.speak(question)

        # Khởi tạo các biến.
        self.porcupine = None
        pa = None
        audio_stream = None

        # Phát hiện từ đánh thức.
        access_key = "08RPO8infyitaLPnJPEfKTK3+l3Cc73mZB2JDtEIVz71RYJ9TOYk/Q=="
        self.porcupine = pvporcupine.create(
            access_key=access_key, keywords=[self.name])

        # Tạo một đối tượng PyAudio.
        pa = pyaudio.PyAudio()

        # Mở luồng tới microphone.
        audio_stream = pa.open(rate=self.porcupine.sample_rate, channels=1, format=pyaudio.paInt16, input=True,
                               frames_per_buffer=self.porcupine.frame_length)

        while True:
            try:
                # Đọc luồng âm thanh và chuyển đổi nó sang định dạng mà porcupine có thể hiểu.
                pcm = audio_stream.read(self.porcupine.frame_length)
                pcm = struct.unpack_from(
                    "h" * self.porcupine.frame_length, pcm)
            except:
                # Mở luồng tới microphone.
                audio_stream = pa.open(rate=self.porcupine.sample_rate, channels=1, format=pyaudio.paInt16, input=True,
                                       frames_per_buffer=self.porcupine.frame_length)

            # Xử lý luồng âm thanh và kiểm tra xem từ khóa có được phát hiện hay không.
            keyword_index = self.porcupine.process(pcm)

            # Trợ lý nghe được từ đánh thức và sau đó lắng nghe đầu vào của người dùng.
            if keyword_index >= 0:
                if audio_stream is not None:
                    with open('samples/answer_assistant.json', encoding='utf-8') as f:
                        data = json.load(f)
                        questions = data.get('', [])
                    question = random.choice(questions)
                    self.answer_signal.emit(question)
                    speaker.speak(question)
                    audio_stream.close()
                said = self.command()

                self.reply(said)

    @pyqtSlot(str)
    def search_on_web(self, query):
        try:
            # API key Google Developer Console
            api_key = "AIzaSyBRx6P6zJN8o6uIxje_AUzFT_OsXJRj-dU"
            # ID của search engine
            search_engine_id = "b3474988609f744f1"

            service = build("customsearch", "v1", developerKey=api_key)
            response = service.cse().list(q=query, cx=search_engine_id, num=1).execute()
            items = response["items"]
            if items:
                return items[0]["link"]
        except Exception as e:
            print(f"Có lỗi xảy ra khi tìm kiếm trên mạng: {str(e)}")

    def replys(self, text, intent):
        with open(f'./samples/{intent}.json', encoding='utf-8') as samplesfile:
            samples = json.load(samplesfile)
        most_similar = determine_most_similar_phrase(
            text=text, intent_dict=samples)

        if type(samples[most_similar]) == str:
            response = samples[most_similar]
            self.answer_signal.emit(response)
            speaker.speak(response)
        elif type(samples[most_similar]) == list:
            response = random.choice(samples[most_similar])
            self.answer_signal.emit(response)
            speaker.speak(response)

    def reply(self, text):
        
        intent = self.intentclassifier.predict(text)

        if intent == 'leaving':
            with open('samples/leaving.json', encoding='utf-8') as f:
                data = json.load(f)
                questions = data.get('', [])
            question = random.choice(questions)
            self.answer_signal.emit(question)
            speaker.speak(question)
            QtWidgets.QApplication.quit()
            sys.exit()

        replies = {
            'greeting': self.replys,
            'tuition': self.replys,
            'department': self.replys,
            'point': self.replys,
            'scholarship': self.replys,
            'pointlookup': point_lookup.main,
            'schedule': schedule.main,
            'sleep': function.main
        }
        if intent in replies:
            reply_func = replies[intent]

            if intent == "sleep":
                self.answer_signal.emit(
                    "Vâng, mình ngủ đây nếu bạn cần mình hãy gọi tên Hey siri")
            elif intent == "pointlookup":
                with open('samples/rp_pl.json', encoding='utf-8') as f:
                    data = json.load(f)
                    self.questions = data.get('', [])
                question = random.choice(self.questions)
                self.answer_signal.emit(question)
                speaker.speak(question)
            elif intent == "schedule":
                with open('samples/access_schedule.json', encoding='utf-8') as f:
                    data = json.load(f)
                    questions = data.get('', [])
                question = random.choice(questions)
                self.answer_signal.emit(question)
                speaker.speak(question)

            # Kiểm tra xem chức năng có thể gọi được không.
            if callable(reply_func):
                reply_func(text, intent)

                with open('samples/ask_again.json', encoding='utf-8') as f:
                    data = json.load(f)
                    questions = data.get('', [])
                question = random.choice(questions)
                self.answer_signal.emit(question)
                speaker.speak(question)
                said = self.command()

                self.reply(said)

        else:
            with open('samples/no_sp.json', encoding='utf-8') as f:
                data = json.load(f)
                questions = data.get('', [])
            question = random.choice(questions)
            self.answer_signal.emit(question)
            speaker.speak(question)

            # Tìm kiếm câu trả lời cho người dùng trên mạng và trả về kết quả
            result = self.search_on_web(text)
            if result:
                with open('samples/info_search.json', encoding='utf-8') as f:
                    data = json.load(f)
                    questions = data.get('', [])
                question = random.choice(questions)
                self.answer_signal.emit(question)
                speaker.speak(question)
                print(result)
                webbrowser.open(result)
                with open('samples/ask_again.json', encoding='utf-8') as f:
                    data = json.load(f)
                    questions = data.get('', [])
                question = random.choice(questions)
                self.answer_signal.emit(question)
                speaker.speak(question)
                said = self.command()

                self.reply(said)
            else:
                question = "Xin lỗi, minh không tìm thấy kết quả trên mạng."
                self.answer_signal.emit(question)
                speaker.speak(question)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(600, 800)

        MainWindow.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        MainWindow.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        icon = QtGui.QIcon("image/assistant_icon.ico")
        MainWindow.setWindowIcon(icon)

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.updateGif)
        self.timer.start(1000)

       # Center main window on screen
        desktop = QtWidgets.QApplication.desktop()
        screen_rect = desktop.screenGeometry()
        x = int((screen_rect.width() - MainWindow.width()) / 2)
        y = int((screen_rect.height() - MainWindow.height()) / 2)
        MainWindow.move(x, y)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # create label
        self.label = QtWidgets.QLabel(self.centralwidget)
        # Giảm kích thước của label
        self.label.setMinimumSize(QtCore.QSize(400, 400))
        # Giảm kích thước của label
        self.label.setMaximumSize(QtCore.QSize(400, 400))
        self.label.setObjectName("label")

        # create text edit
        self.answer_text = QtWidgets.QTextEdit(self.centralwidget)
        self.answer_text.setReadOnly(True)

        self.answer_text.setStyleSheet("""
            QTextEdit {
                background-color: rgba(255, 255, 255, 200);
                border: 1px solid rgba(0, 0, 0, 0.2);
                border-radius: 20px;
                padding: 10px;
            }
        """)
        self.answer_text.setFixedHeight(150)
        self.answer_text.setFixedWidth(300)
        self.answer_text.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.answer_text.setVerticalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)

        # create grid layout
        layout = QtWidgets.QGridLayout(self.centralwidget)
        layout.addWidget(self.label, 0, 0, alignment=QtCore.Qt.AlignCenter)
        # Khung QTextEdit nằm bên phải của label
        layout.addWidget(self.answer_text, 0, 1)

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
            self.answer_text.show()
        else:
            self.label.clear()
            self.answer_text.hide()

    def paintEvent(self, event):
        painter = QtGui.QPainter(self.viewport())
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(self.palette().base())
        painter.drawRoundedRect(self.rect(), 20, 20)

        super().paintEvent(event)


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()

        # Giao diện
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Khởi tạo trợ lý và đa luồng trợ lý
        self.assistant = AssistantThread("hey siri")
        self.assistant.answer_signal.connect(self.add_answer_item)
        self.assistant.start()

    def add_answer_item(self, answer):
        # Thiết lập kích thước font chữ là 13
        self.ui.answer_text.setFontPointSize(13)
        # Xóa nội dung hiện tại của QTextEdit
        self.ui.answer_text.clear()
        # Thêm câu trả lời mới vào QTextEdit
        self.ui.answer_text.append(answer)

        # Di chuyển con trỏ đến cuối văn bản
        self.ui.answer_text.moveCursor(QtGui.QTextCursor.End)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
