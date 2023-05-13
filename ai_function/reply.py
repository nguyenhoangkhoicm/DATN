import json,random
from ai_function.determine_most_similar import determine_most_similar_phrase
from ai_function.speaklisten import speaker

def reply(text, intent):
    """
    Lấy văn bản chứa ý định làm đầu vào, mở tệp json với tên ý định, xác định 
    cụm từ tương tự trong tệp json, rồi đọc câu trả lời.
    :param text: Văn bản mà người dùng đã nói
    :param intent: ý định của đầu vào của người dùng
    """
    with open(f'./samples/{intent}.json', encoding='utf-8') as samplesfile:
        samples = json.load(samplesfile)
    most_similar = determine_most_similar_phrase(
        text=text, intent_dict=samples)

    if type(samples[most_similar]) == str:
        speaker.speak(samples[most_similar])
    elif type(samples[most_similar]) == list:
        speaker.speak(random.choice(samples[most_similar]))
