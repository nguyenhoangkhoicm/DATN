
import json
import random

from ai_function.determine_most_similar import determine_most_similar_phrase
from ai_function.speaklisten import speaker


def reply(text, intent):

    with open(f'./samples/{intent}.json', encoding='utf-8') as samplesfile:
        samples = json.load(samplesfile)
    most_similar = determine_most_similar_phrase(
        text=text, intent_dict=samples)

    if type(samples[most_similar]) == str:
        speaker.speak(samples[most_similar])
    elif type(samples[most_similar]) == list:
        speaker.speak(random.choice(samples[most_similar]))


"""
Hàm reply mở một tệp JSON có tên là intent.json trong thư mục samples và đọc nội dung của tệp này vào một biến có tên là samples.
Sau đó, hàm này sử dụng hàm determine_most_similar_phrase từ mô-đun ai_function.determine_most_similar để tìm khóa của từ điển samples có giá trị tương đồng cao nhất với chuỗi ký tự text. 
Khóa này được lưu trữ trong biến most_similar.

Tiếp theo, hàm kiểm tra xem giá trị của khóa most_similar trong từ điển samples có phải là một chuỗi ký tự hay một danh sách hay không. 
Nếu giá trị đó là một chuỗi ký tự, hàm sẽ sử dụng phương thức speak của đối tượng speaker từ mô-đun ai_function.speaklisten để đọc giá trị đó. Nếu giá trị đó là một danh sách, hàm sẽ chọn ngẫu nhiên một phần tử trong danh sách và sử dụng phương thức speak để đọc phần tử đó.
"""
