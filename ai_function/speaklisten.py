
from gtts import gTTS
import playsound
import os
import re
import webbrowser
import speech_recognition as sr
import pvporcupine
import struct
import pyaudio


class speaker(object):

    def speak(text):

        urls = re.findall(r'https\S+', text)
        for url in urls:
            webbrowser.open(url)
        text = re.sub(r'https\S+', '', text)

        print("🤖: " + text)

        tts = gTTS(text=text, lang='vi', slow=False)

        tts.save('voice.mp3')
        playsound.playsound('voice.mp3')
        os.remove('voice.mp3')

        return text

    def siri():
        name = "hey siri"
        #  khởi tạo các biến.
        porcupine = None
        pa = None
        audio_stream = None

        # Phát hiện từ đánh thức.
        access_key = "08RPO8infyitaLPnJPEfKTK3+l3Cc73mZB2JDtEIVz71RYJ9TOYk/Q=="
        porcupine = pvporcupine.create(
            access_key=access_key, keywords=[name])

        # Tạo một đối tượng PyAudio.
        pa = pyaudio.PyAudio()

        # mở luồng tới micrô.
        audio_stream = pa.open(
            rate=porcupine.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=porcupine.frame_length)

        while True:

            try:
                # Đọc luồng âm thanh và chuyển đổi nó sang định dạng mà porcupine có thể
                # hiểu.
                pcm = audio_stream.read(porcupine.frame_length)
                pcm = struct.unpack_from(
                    "h" * porcupine.frame_length, pcm)
            except:
                # mở luồng tới micrô.
                audio_stream = pa.open(
                    rate=porcupine.sample_rate,
                    channels=1,
                    format=pyaudio.paInt16,
                    input=True,
                    frames_per_buffer=porcupine.frame_length)

            # Xử lý luồng âm thanh và kiểm tra xem từ khóa có được phát hiện hay không.
            keyword_index = porcupine.process(pcm)

            # Trợ lý nghe được từ đánh thức và sau đó lắng nghe đầu vào của người dùng.
            if keyword_index >= 0:
                if audio_stream is not None:

                    audio_stream.close()
                break

    def command(count=0):
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
