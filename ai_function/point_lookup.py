
from ai_function.determine_most_similar import determine_most_similar_phrase
from ai_function.speaklisten import speaker

from selenium import webdriver
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.common.by import By
from tkinter import Tk
from tkinter import simpledialog
from bs4 import BeautifulSoup

import speech_recognition as sr
import pandas as pd
import openpyxl
import os
import json


class point_lookup():
    def main(self, text, intent):
        task = self.determine_search_or_open(text)
        if task == 'pointlookup':
            self.point()

    def determine_search_or_open(self, text):
        with open('samples/phrases_point.json', 'r', encoding='utf-8') as file:
            phrases = json.load(file)
        most_similar = determine_most_similar_phrase(text, phrases)
        return phrases[most_similar]

    def point(self):

        # with open('samples/rp_pl.json', encoding='utf-8') as f:
        #     data = json.load(f)
        #     self.questions = data.get('', [])
        # question = random.choice(self.questions)
        # speaker.speak(question)

        # Khởi tạo trình duyệt
        driver = webdriver.Edge()

        # Truy cập vào trang web
        driver.get("https://camau.bdu.edu.vn/tracuudiem/index.php")

        # Yêu cầu người dùng nhập mã số sinh viên bằng giọng nói
        speaker.speak("Vui lòng nói mã số sinh viên")

        try:
            student_id = speaker.command()
            student_id = student_id.replace(" ", "")  # Loại bỏ khoảng trắng
            # Nhập mã số sinh viên vào thẻ input có id="fname"
            student_id_input = driver.find_element(By.ID, "fname")
            student_id_input.send_keys(student_id)
        except sr.UnknownValueError:
            speaker.speak("Không nhận dạng được giọng nói. Vui lòng thử lại.")
            return None
        except sr.RequestError:
            speaker.speak("Lỗi kết nối Internet. Vui lòng kiểm tra lại.")
            return None

        while True:
            # Yêu cầu người dùng nhập mã bảo vệ bằng giọng nói
            speaker.speak("Vui lòng nhập mã bảo vệ.")
            root = Tk()
            root.withdraw()
            captcha = simpledialog.askstring(
                'Captcha', 'Enter captcha:', parent=root)
            captcha_input = driver.find_element(By.ID, "captcha")
            captcha_input.send_keys(captcha)

            # Click vào thẻ input có name="remember"
            remember_checkbox = driver.find_element(By.NAME, "remember")
            remember_checkbox.click()

            # Click vào button có name="send"
            send_button = driver.find_element(By.NAME, "send")
            send_button.click()

            # Kiểm tra xem có thông báo lỗi hay không
            try:
                alert = driver.switch_to.alert
                alert_text = alert.text
                if "Nhập sai mã bảo vệ!!!" in alert_text:
                    alert.accept()
                    # Yêu cầu người dùng nói lại mã số sinh viên
                    speaker.speak(
                        "Vì bạn nhập sai mã sinh viên hoặc mã bảo vệ nên bạn phải nói lại mã số sinh viên của mình và nhập lại mã bảo vệ mới.")

                    try:
                        student_id = speaker.command()
                        student_id = student_id.replace(
                            " ", "")  # Loại bỏ khoảng trắng
                        # Nhập mã số sinh viên vào thẻ input có id="fname"
                        student_id_input = driver.find_element(By.ID, "fname")
                        # student_id_input.clear()  # Xóa nội dung hiện tại
                        student_id_input.send_keys(student_id)
                    except sr.UnknownValueError:
                        speaker.speak(
                            "Không nhận dạng được giọng nói. Vui lòng thử lại.")
                        continue
                    except sr.RequestError:
                        speaker.speak(
                            "Lỗi kết nối Internet. Vui lòng kiểm tra lại.")
                        continue
                    # Yêu cầu người dùng nhập lại mã bảo vệ
                    while True:
                        speaker.speak("Nhập mã bảo vệ lại")
                        root = Tk()
                        root.withdraw()
                        captcha = simpledialog.askstring(
                            'Captcha', 'Enter captcha:', parent=root)
                        captcha_input = driver.find_element(By.ID, "captcha")
                        # captcha_input.clear()  # Xóa nội dung hiện tại
                        captcha_input.send_keys(captcha)

                        # Click vào thẻ input có name="remember"
                        remember_checkbox = driver.find_element(
                            By.NAME, "remember")
                        remember_checkbox.click()

                        # Click vào button có name="send"
                        send_button = driver.find_element(By.NAME, "send")
                        send_button.click()
                        break

                        # Kiểm tra xem có thông báo lỗi hay không
                    try:
                        alert = driver.switch_to.alert
                        alert_text = alert.text
                        if "Nhập sai mã bảo vệ!!!" in alert_text:
                            alert.accept()
                            continue
                        else:
                            break
                    except NoAlertPresentException:
                        break

                else:
                    break
            except NoAlertPresentException:
                break

        # Lấy nội dung trang web
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')

        # Tìm tất cả các bảng HTML với thuộc tính class bằng "table table-striped table-hover tapble"
        tables = soup.find_all(
            'table', {'class': 'table table-striped table-hover tapble'})

        data = []
        for table in tables:
            # Lấy tiêu đề h3
            headers = [header.text for header in table.find_all('th')]
            h3 = table.find_previous_sibling('h3')
            if h3:
                data.append([h3.text])

            # Lấy dữ liệu trong bảng
            for row in table.find_all('tr'):
                data.append([cell.text for cell in row.find_all('td')])

        # # Lưu dữ liệu vào file excel
        df = pd.DataFrame(data, columns=headers)
        df.to_excel('output.xlsx', index=False)

        # Thêm thông tin của thẻ <th> vào đầu file Excel
        th = soup.find('th', {'class': 'myth'})
        if th:
            # Mở file Excel
            book = openpyxl.load_workbook('output.xlsx')
            sheet = book.active

            # Chèn một hàng mới vào đầu bảng
            sheet.insert_rows(1)

            # Gán giá trị cho ô A1
            sheet['A1'] = th.text

            # Lưu lại file Excel
            book.save('output.xlsx')

        driver.quit()
        os.system('start output.xlsx')
        speaker.speak('Đây là bảng điểm của bạn')


point_lookup = point_lookup()
