
from difflib import SequenceMatcher


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


"""
Hàm how_similar(a, b) nhận vào hai chuỗi ký tự a và b và trả về tỷ lệ tương đồng giữa chúng dưới dạng một số nguyên. 
Hàm này sử dụng lớp SequenceMatcher của mô-đun difflib để tính tỷ lệ tương đồng giữa hai chuỗi.

Hàm determine_most_similar_phrase(text, intent_dict) nhận vào một chuỗi ký tự text và một từ điển intent_dict chứa các cặp khóa-giá trị. 
Hàm này tìm khóa của từ điển có giá trị tương đồng cao nhất với chuỗi ký tự text và trả về khóa đó. Hàm này sử dụng hàm how_similar để tính tỷ lệ tương đồng giữa text và các khóa của từ điển.
"""
