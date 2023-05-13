
from difflib import SequenceMatcher
# import random

def how_similar(a, b):
    # Hàm how_similar(a, b) tính tỷ lệ tương đồng giữa hai chuỗi ký tự a và b
    return int(SequenceMatcher(None, a, b).ratio()*100)

def determine_most_similar_phrase(text, intent_dict):
    # Hàm determine_most_similar_phrase(text, intent_dict) tìm ý định của intent_dict có giá trị tương đồng cao nhất với chuỗi ký tự text.
    my_list = []
    my_dict = {}
    if len(intent_dict) == 1:
        for key, value in intent_dict.items():
            return key

    elif len(intent_dict) > 1:
        for key,  value in intent_dict.items():
            my_list.append(value)
            my_dict.update({key: how_similar(text.lower(), key)})
        sorted_dict = sorted(
            my_dict.items(),  key=lambda x: x[1], reverse=True)
        what_user_is_saying = list(sorted_dict[0])[0]
        return what_user_is_saying
