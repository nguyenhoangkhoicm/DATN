from ai_function.access_schedule import schedule
from ai_function.speaklisten import speaker
from ai_function.point_lookup import point_lookup
from ai_function.reply import reply
from intentclassification.intent_classification import IntentClassifier

import pyaudio
import json
import random
import sys
import struct
import pvporcupine
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import pyqtSlot


class AssistantThread(QtCore.QThread):
    answer_signal = QtCore.pyqtSignal(str)

    def __init__(self, name):
        super().__init__()
        self.name = name
        self.intentclassifier = IntentClassifier()

    def run(self):

        with open('samples/hello_assistant.json', encoding='utf-8') as f:
            data = json.load(f)
            self.questions = data.get('', [])

        question = random.choice(self.questions)
        speaker.speak(question)
        self.answer_signal.emit(question)

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
        audio_stream = pa.open(
            rate=self.porcupine.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=self.porcupine.frame_length)

        while True:
            try:
                # Đọc luồng âm thanh và chuyển đổi nó sang định dạng mà porcupine có thể hiểu.
                pcm = audio_stream.read(self.porcupine.frame_length)
                pcm = struct.unpack_from(
                    "h" * self.porcupine.frame_length, pcm)
            except:
                # Mở luồng tới microphone.
                audio_stream = pa.open(
                    rate=self.porcupine.sample_rate,
                    channels=1,
                    format=pyaudio.paInt16,
                    input=True,
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

                said = speaker.command()  # Lắng nghe đầu vào của người dùng
                self.reply(said)
                self.answer_signal.emit(said)

    @pyqtSlot(str)
    def reply(self, text):

        intent = self.intentclassifier.predict(text)

        if intent == 'leaving':
            speaker.speak("Rất vui được phục vụ bạn.")
            self.answer_signal.emit("Rất vui được phục vụ bạn.")
            sys.exit()

        replies = {
            'greeting': reply,
            'insult': reply,
            'install': reply,
            'tuition': reply,
            'department': reply,
            'point': reply,
            'pointlookup': point_lookup.main,
            'schedule': schedule.main

        }
        if intent in replies:
            reply_func = replies[intent]

            # Kiểm tra xem chức năng có thể gọi được không.
            if callable(reply_func):
                reply_func(text, intent)

                with open('samples/ask_again.json', encoding='utf-8') as f:
                    data = json.load(f)
                    questions = data.get('', [])
                question = random.choice(questions)
                self.answer_signal.emit(question)
                speaker.speak(question)
                said = speaker.command()
                self.answer_signal.emit(said)
                self.reply(said)

        else:
            speaker.speak("Xin lỗi mình chưa đủ thông minh để giúp bạn😣😣")


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        # Khởi tạo các widget và thiết lập giao diện
        self.answer_list = QtWidgets.QListWidget()

        central_widget = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(central_widget)
        layout.addWidget(self.answer_list)

        self.setCentralWidget(central_widget)

        # Khởi tạo trợ lý và đa luồng trợ lý
        self.assistant = AssistantThread("hey siri")
        self.assistant.answer_signal.connect(self.add_answer_item)
        self.assistant.start()  # Bắt đầu chạy đa luồng

    def add_answer_item(self, answer):
        item = QtWidgets.QListWidgetItem(answer)
        self.answer_list.addItem(item)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Return:
            text = self.input_text.toPlainText()
            reply = self.assistant.reply(text)

            # Thêm câu trả lời vào danh sách
            self.add_answer_item(reply)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
