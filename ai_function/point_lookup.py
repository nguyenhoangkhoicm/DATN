from ai_function.determine_most_similar import determine_most_similar_phrase
from ai_function.speaklisten import speaker
from selenium import webdriver
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.common.by import By
from tkinter import Tk ,simpledialog
from bs4 import BeautifulSoup

import speech_recognition as sr
import pandas as pd

class point_lookup():
    def main(self, text, intent):
        task = self.determine_search_or_open(text)
        if task == 'pointlookup':
            self.point()

    def determine_search_or_open(self, text):
        phrases = {
            "Bạn xem điểm số giúp mình": "pointlookup",
            "Bạn xem điểm giúp mình":"pointlookup",
            "Bạn cho mình xem bảng điểm với":"pointlookup",
            "Bạn có thể cho tôi xem bảng điểm của tôi được không":"pointlookup",
            "Tôi muốn xem bảng điểm của mình":"pointlookup",
            "Bạn có thể giúp tôi xem bảng điểm được không":"pointlookup",
            "Tôi cần xem bảng điểm của mình":"pointlookup",
            "Bạn vui lòng cho tôi xem bảng điểm của tôi":"pointlookup",
            "Tôi muốn kiểm tra bảng điểm của mình":"pointlookup",
            "Tôi muốn biết điểm số của mình trong bảng điểm":"pointlookup"
            
        }

        most_similar = determine_most_similar_phrase(text, phrases)
        return phrases[most_similar]

    def point(self):
        # Khởi tạo trình duyệt
        driver = webdriver.Chrome()

        # Truy cập vào trang web
        driver.get("https://camau.bdu.edu.vn/tracuudiem/index.php")

        # Khởi tạo đối tượng nhận dạng giọng nói
        recognizer = sr.Recognizer()

        # Yêu cầu người dùng nhập mã số sinh viên bằng giọng nói
        speaker.speak("Vui lòng nói mã số sinh viên:")
        with sr.Microphone() as source:
            audio = recognizer.listen(source)
        student_id = recognizer.recognize_google(audio, language="vi-VN")
        student_id = student_id.replace(" ", "")  # Loại bỏ khoảng trắng
        # print(f"Mã số sinh viên: {student_id}")

        # Nhập mã số sinh viên vào thẻ input có id="fname"
        student_id_input = driver.find_element(By.ID,"fname")
        student_id_input.send_keys(student_id)

        # Yêu cầu người dùng nhập mã bảo vệ bằng giọng nói
        while True:
    # Yêu cầu người dùng nhập mã bảo vệ bằng giọng nói
            speaker.speak("Vui nhập mã bảo vệ.")
            root = Tk()
            root.withdraw()
            captcha = simpledialog.askstring('Captcha', 'Enter captcha:', parent=root)
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
                    continue
                else:
                    break
            except NoAlertPresentException:
                break

        # root = Tk()
        # root.withdraw()
        # captcha = simpledialog.askstring('Captcha', 'Enter captcha:', parent=root)
        # captcha_input = driver.find_element(By.ID,"captcha")
        # captcha_input.send_keys(captcha)

        # # Click vào thẻ input có name="remember"
        # remember_checkbox = driver.find_element(By.NAME,"remember")
        # remember_checkbox.click()

        # # Click vào button có name="send"
        # send_button = driver.find_element(By.NAME,"send")
        # send_button.click()

        # Lấy nội dung trang web
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')

        # Tìm tất cả các bảng HTML với thuộc tính class bằng "table table-striped table-hover tapble"
        tables = soup.find_all('table', {'class': 'table table-striped table-hover tapble'})


        import openpyxl
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

        # Lưu dữ liệu vào file excel
        df = pd.DataFrame(data,columns=headers)
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

        import os
        os.system('start output.xlsx')
        speaker.speak('Đây là bảng điểm của bạn')


point_lookup= point_lookup()