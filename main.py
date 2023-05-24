from ai_function.access_schedule import schedule
from ai_function.speaklisten import speaker
from ai_function.point_lookup import point_lookup
from ai_function.sleep import function
from ai_function.reply import reply
from intentclassification.intent_classification import IntentClassifier

import pyaudio,json,random,sys,struct,pvporcupine

class Assistant:
    
    def __init__(self, name):
        self.name = name
        
    def reply(self, text):
        """
        Nếu ý định là 'rời đi', thì trợ lý nói "rất vui được phục vụ bạn." và thoát chương trình. 
        Nếu không, gọi chức năng trong mục /ai_function trả lời tương ứng với mục đích của người dùng.

        :param text: Văn bản mà người dùng đã nhập
        """
        intent = intentclassifier.predict(text)
        
        if intent == 'leaving':
            with open('samples/leaving.json',encoding='utf-8') as f:
                    data = json.load(f)
                    questions = data.get('', [])
            question = random.choice(questions)
            speaker.speak(question)
            sys.exit()
      
        replies = {
            'greeting': reply,
            'tuition':reply,
            'department':reply,
            'point':reply,
            'pointlookup':point_lookup.main,
            'schedule': schedule.main,
            'sleep':function.main
        }
        if intent in replies:
            reply_func = replies[intent]

            # Kiểm tra xem chức năng có thể gọi được không.
            if callable(reply_func):
                reply_func(text, intent)
                with open('samples/ask_again.json',encoding='utf-8') as f:
                    data = json.load(f)
                    questions = data.get('', [])
                question = random.choice(questions)
                speaker.speak(question)
                said=speaker.command()
                self.reply(said)
             
        else:
            speaker.speak("Xin lỗi mình chưa đủ thông minh để giúp bạn")
 
    def main(self):

        with open('samples/hello_assistant.json',encoding='utf-8') as f:
            data = json.load(f)
            self.questions = data.get('', [])

        question = random.choice(self.questions)
        speaker.speak(question)
        
        #  khởi tạo các biến.
        self.porcupine = None
        pa = None
        audio_stream = None

        # Phát hiện từ đánh thức.
        access_key = "08RPO8infyitaLPnJPEfKTK3+l3Cc73mZB2JDtEIVz71RYJ9TOYk/Q=="
        self.porcupine = pvporcupine.create(
            access_key=access_key, keywords=[self.name])

        # Tạo một đối tượng PyAudio.
        pa = pyaudio.PyAudio()

        # mở luồng tới micrô.
        audio_stream = pa.open(
            rate=self.porcupine.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=self.porcupine.frame_length)

        while True:

            try:
                # Đọc luồng âm thanh và chuyển đổi nó sang định dạng mà porcupine có thể
                # hiểu.
                pcm = audio_stream.read(self.porcupine.frame_length)
                pcm = struct.unpack_from(
                    "h" * self.porcupine.frame_length, pcm)
            except:
                # mở luồng tới micrô.
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
                    with open('samples/answer_assistant.json',encoding='utf-8') as f:
                        data = json.load(f)
                        questions= data.get('', [])
                    question = random.choice(questions)
                    speaker.speak(question)
                    audio_stream.close()
                    
                said = speaker.command()  # Lắng nghe đầu vào của người dùng
                self.reply(said)

# Gọi chức năng chính của lớp Trợ lý.
intentclassifier = IntentClassifier()
assistant = Assistant("hey siri")
assistant.main()



