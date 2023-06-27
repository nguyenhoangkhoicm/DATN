from difflib import SequenceMatcher


def how_similar(a, b):
    # Hàm how_similar(a, b) tính tỷ lệ tương đồng giữa hai chuỗi ký tự a và b
    return SequenceMatcher(None, a, b).ratio()


def determine_most_similar_phrase(text, intent_dict):
    # Hàm determine_most_similar_phrase(text, intent_dict) tìm ý định của intent_dict có giá trị tương đồng cao nhất với chuỗi ký tự text.
    max_similarity = 0
    most_similar_intent = None

    text = text.lower()  # Chuyển đổi chuỗi về chữ thường

    for intent, value in intent_dict.items():
        similarity = how_similar(text, intent.lower())  # So sánh chuỗi

        if similarity > max_similarity:
            max_similarity = similarity
            most_similar_intent = intent

    return most_similar_intent
