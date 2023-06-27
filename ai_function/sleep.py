from ai_function.determine_most_similar import determine_most_similar_phrase
from ai_function.speaklisten import speaker

import json


class function():

    def main(self, text, intent):
        task = self.determine_search_or_open(text)
        if task == 'sleep':
            self.func()

    def determine_search_or_open(self, text):
        with open('samples/phrases_sleep.json', 'r', encoding='utf-8') as file:
            phrases = json.load(file)
        most_similar = determine_most_similar_phrase(text, phrases)
        return phrases[most_similar]

    def func(self):
        response = "Vâng, mình ngủ đây nếu bạn cần mình hãy gọi tên Hey siri"
        speaker.speak(response)

        while True:
            try:
                speaker.siri()
                break
            except:
                pass


function = function()
