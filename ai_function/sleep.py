from ai_function.determine_most_similar import determine_most_similar_phrase
from ai_function.speaklisten import speaker

class function():
    def main(self, text, intent):
        task = self.determine_search_or_open(text)
        if task == 'sleep':
            self.func()

    def determine_search_or_open(self, text):
        phrases = {
            "bạn ngủ đi": "sleep",
            "Trợ lý ơi hãy đi ngủ đi": "sleep",
            "Lúc này trợ lý nên đi nghỉ một chút": "sleep",
            "Hãy tắt đi và nghỉ ngơi trợ lý": "sleep",
            "Trợ lý hãy ngủ một giấc để sạc năng lượng": "sleep",
            "Bạn cần một giấc ngủ ngon trợ lý ơi": "sleep",
            "Hãy để tôi và bạn ngủ trợ lý": "sleep",
            "Bạn đã làm việc chăm chỉ giờ hãy nghỉ ngơi đi trợ lý": "sleep",
            "Trợ lý đến giờ đi nghỉ rồi": "sleep",
            "Hãy cùng nghỉ ngơi trợ lý ơi": "sleep",
            "Đi ngủ thôi trợ lý": "sleep",
            "Bạn đã làm tốt giờ hãy nghỉ ngơi trợ lý ạ": "sleep",
            "Trợ lý hãy dừng lại và nghỉ ngơi một chút": "sleep",
            "Giờ là lúc đi ngủ trợ lý": "sleep",
            "Trợ lý cần một giấc ngủ tốt để cập nhật thông tin mới": "sleep",
            "Hãy để tôi giải quyết trợ lý hãy đi ngủ đi": "sleep",
            "Tôi sẽ lo công việc còn trợ lý thì hãy đi nghỉ ngơi": "sleep",
            "Trợ lý đến giờ nghỉ ngơi rồi": "sleep",
            "Hãy để tôi chăm sóc công việc trợ lý đi ngủ đi": "sleep",
            "Trợ lý cần thời gian nghỉ ngơi hãy đi ngủ ngay": "sleep",
            "Bạn đã làm rất tốt bây giờ hãy nghỉ ngơi trợ lý": "sleep",
            "Trợ lý ơi cần một giấc ngủ ngon lành": "sleep",
            "Đến lúc đi ngủ rồi trợ lý": "sleep",
            "Hãy tắt đi và nghỉ ngơi trợ lý ạ": "sleep",
            "Bạn cần giấc ngủ để tươi tắn trợ lý": "sleep",
            "Trợ lý cần sức khỏe hãy đi ngủ ngay": "sleep",
            "Đến giờ nghỉ ngơi rồi trợ lý ơi": "sleep",
            "Hãy để tôi lo công việc trợ lý hãy đi ngủ đi": "sleep",
            "Trợ lý hãy nghỉ ngơi một chút để sạc lại năng lượng": "sleep",
            "Bạn đã làm việc hết sức giờ hãy nghỉ ngơi trợ lý": "sleep",
            "Trợ lý cần một giấc ngủ tốt cho cơ thể": "sleep",
            "Hãy để tôi chịu trách nhiệm trợ lý hãy đi ngủ đi": "sleep",
            "Trợ lý cần thời gian nghỉ ngơi hãy tắt đi": "sleep",
            "Bạn đã làm rất tốt bây giờ hãy nghỉ ngơi trợ lý": "sleep",
            "Trợ lý ơi cần một giấc ngủ ngon lành": "sleep",
            "Đến lúc đi ngủ rồi trợ lý": "sleep",
            "Hãy tắt đi và nghỉ ngơi trợ lý ạ": "sleep",
            "Bạn cần giấc ngủ để tươi tắn trợ lý": "sleep",
            "Trợ lý cần sức khỏe hãy đi ngủ ngay": "sleep",
            "Đến giờ nghỉ ngơi rồi trợ lý ơi": "sleep",
            "Hãy để tôi lo công việc trợ lý hãy đi ngủ đi": "sleep",
            "Trợ lý hãy nghỉ ngơi một chút để sạc lại năng lượng": "sleep",
            "Bạn đã làm việc hết sức giờ hãy nghỉ ngơi trợ lý": "sleep",
            "Trợ lý cần một giấc ngủ tốt cho cơ thể": "sleep",
            "Hãy để tôi chịu trách nhiệm trợ lý hãy đi ngủ đi": "sleep",
            "Trợ lý cần thời gian nghỉ ngơi hãy tắt đi": "sleep",
            "Bạn đã làm rất tốt bây giờ hãy nghỉ ngơi trợ lý": "sleep",
            "Trợ lý ơi cần một giấc ngủ ngon lành": "sleep",
            "Đến lúc đi ngủ rồi trợ lý": "sleep",
            "Hãy tắt đi và nghỉ ngơi trợ lý ạ": "sleep",
            "Bạn cần ngủ đi": "sleep"
        }

        most_similar = determine_most_similar_phrase(text, phrases)
        return phrases[most_similar]

    def func(self):
        speaker.speak("Vâng, mình ngủ đây nếu bạn cần mình hãy gọi tên 'Hey siri'")         
        while True:
            try:
                speaker.siri() 
                break
            except:
                pass

function = function()
