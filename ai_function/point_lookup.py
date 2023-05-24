from ai_function.determine_most_similar import determine_most_similar_phrase
from ai_function.speaklisten import speaker
from selenium import webdriver
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.common.by import By
from tkinter import Tk, simpledialog
from bs4 import BeautifulSoup

import speech_recognition as sr
import pandas as pd
import openpyxl
import os,random,json


class point_lookup():
    def main(self, text, intent):
        task = self.determine_search_or_open(text)
        if task == 'pointlookup':
            self.point()

    def determine_search_or_open(self, text):
        phrases = {
            "Bạn xem điểm số giúp mình": "pointlookup",
            "Bạn xem điểm giúp mình": "pointlookup",
            "Bạn cho mình xem bảng điểm với": "pointlookup",
            "Bạn có thể cho tôi xem bảng điểm của tôi được không": "pointlookup",
            "Tôi muốn xem bảng điểm của mình": "pointlookup",
            "Bạn có thể giúp tôi xem bảng điểm được không": "pointlookup",
            "Tôi cần xem bảng điểm của mình": "pointlookup",
            "Bạn vui lòng cho tôi xem bảng điểm của tôi": "pointlookup",
            "Tôi muốn kiểm tra bảng điểm của mình": "pointlookup",
            "Tôi muốn biết điểm số của mình trong bảng điểm": "pointlookup",
            "Bạn có thể giúp tôi xem điểm số được không ": "pointlookup",
            "Tôi cần kiểm tra điểm số của mình bạn có thể giúp tôi xem lại được không ": "pointlookup",
            "Tôi muốn biết điểm số của mình bạn có thể xem giúp tôi ": "pointlookup",
            "Bạn có thể gửi cho tôi bảng điểm của mình qua email được không ": "pointlookup",
            "Tôi cần xem điểm số để biết mình đã đạt được mục tiêu học tập hay chưa": "pointlookup",
            "Tôi muốn biết điểm số của mình để có thể cải thiện kết quả học tập": "pointlookup",
            "Tôi không nhớ điểm số của mình bạn có thể giúp tôi xem lại được không ": "pointlookup",
            "Tôi đang cần xem điểm số để chuẩn bị cho kỳ thi tốt nghiệp ,pointlookup9. Tôi muốn biết điểm số của mình để chuẩn bị cho cuộc phỏng vấn tuyển dụng": "pointlookup",
            "Bạn có thể giúp tôi xem điểm số để đánh giá khả năng được nhận học bổng không ": "pointlookup",
            "Tôi cần xem điểm số để biết mình còn thiếu những kỹ năng nào trong lĩnh vực học tập của mình": "pointlookup",
            "Tôi muốn xem điểm số để biết mình đã tiến bộ đáng kể hay chưa trong học tập": "pointlookup",
            "Tôi cần biết điểm số của mình để có thể đưa ra phương án học tập phù hợp hơn": "pointlookup",
            "Tôi muốn xem điểm số để biết mình có cần thay đổi phương pháp học tập hay không": "pointlookup",
            "Tôi cần xem điểm số để chuẩn bị cho cuối kỳ học tập": "pointlookup",
            "Tôi muốn biết điểm sốcủa mình để cải thiện kết quả trong các môn học tiếp theo": "pointlookup",
            "Tôi cần xem điểm số để biết mình đã đạt yêu cầu đầu vào của các chương trình học tập": "pointlookup",
            "Tôi muốn xem điểm số để đánh giá năng lực của mình trong lĩnh vực học tập": "pointlookup",
            "Tôi cần xem điểm số để biết mình đã đáp ứng được yêu cầu của giảng viên hay chưa": "pointlookup",
            "Tôi muốn biết điểm số của mình để có thể đưa ra phương án học tập phù hợp hơn trong tương lai": "pointlookup",
            "Tôi cần xem điểm số để có thể chuẩn bị cho các kỳ thi tiếp theo": "pointlookup",
            "Tôi muốn xem điểm số để biết mình có năng lực để đạt được các chứng chỉ liên quan đến lĩnh vực học tập của mình hay không": "pointlookup",
            "Tôicần xem điểm số để đánh giá mức độ hiệu quả của phương pháp học tập mà tôi đang áp dụng": "pointlookup",
            "Tôi muốn biết điểm số của mình để có thể đưa ra phương án học tập phù hợp hơn trong kỳ học tiếp theo": "pointlookup",
            "Tôi cần xem điểm số để biết mình đã đáp ứng được các tiêu chí đánh giá của chương trình học tập hay chưa": "pointlookup",
            "Tôi muốn xem điểm số để biết mình đã đạt được các mục tiêu học tập mình đề ra hay chưa": "pointlookup",
            "Tôi cần xem điểm số để có thể chuẩn bị cho kế hoạch học tập trong tương lai": "pointlookup",
            "Tôi muốn biết điểm số để có thể cải thiện mối quan hệ với giảng viên và các bạn cùng học": "pointlookup",
            "Tôi cần xem điểm số để đánh giá khả năng của mình trong việc theo đuổi con đường học tập": "pointlookup",
            "Tôi muốn xem điểm số để biết mình có cần tăng cường kiến thức hay không": "pointlookup",
            "Tôi cần xem điểm số để có thể đưa ra phương án học tập phù hợp hơn trong tương lai": "pointlookup",
            "Tôi muốn biết điểm số để xác định mức độ thành công trong học tập của mình": "pointlookup",
            "Tôi cần xem điểm số để biết mình cần cải thiện điểm số ở những môn nào": "pointlookup",
            "Tôi muốn xem điểm số để biết mình đã đạt được mục tiêu học tập của mình hay chưa": "pointlookup",
            "Tôi cần xem điểm số để biết mình nên tập trung vào những môn học nào trong tương lai": "pointlookup",
            "Tôi muốn biết điểm số để có thể đưa ra phương án học tập phù hợp hơn trong kỳ học tiếp theo": "pointlookup",
            "Tôi cần xem điểm số để đánh giá năng lực của mình trong các lĩnh vực học tập khác nhau": "pointlookup",
            "Tôi muốn xem điểm số để biết mình có cần tăng cường kỹ năng học tập hay không": "pointlookup",
            "Tôi cần xem điểm số để biết mình đã đạt được các tiêu chuẩn đánh giá của chương trình học tập hay chưa": "pointlookup",
            "Tôi muốn biết điểm số để có thể đưa ra phương án học tập phù hợp hơn cho tương lai": "pointlookup",
            "Tôi cần xem điểm số để biết mình đã đáp ứng được yêu cầu của giảng viên trong các bài kiểm tra hay không": "pointlookup",
            "Tôi muốn xem điểm số để biết mình có đủ năng lực để theo đuổi các chương trình học tập khác nhau": "pointlookup",
            "Tôi cần xemđiểm số để biết mình cần cải thiện điểm số ở những môn học nào để có được kết quả tốt hơn": "pointlookup",
            "Tôi muốn biết điểm số của mình để có thể đưa ra phương án học tập phù hợp hơn với mục tiêu nghề nghiệp của mình": "pointlookup",
            "Tôi cần xem điểm số để biết mình đã đạt được các tiêu chí đánh giá của nhà tuyển dụng hay chưa": "pointlookup",
            "Tôi muốn xem điểm số để biết mình có năng lực để theo đuổi các khóa học chuyên ngành hay không": "pointlookup",
            "Tôi cần xem điểm số để biết mình cần cải thiện điểm số ở những môn học mà mình đang yếu": "pointlookup",
            "Tôi muốn biết điểm số của mình để có thể đưa ra phương án học tập phù hợp hơn với kế hoạch sự nghiệp của mình": "pointlookup",
            "Tôi cần xem điểm số để biết mình có đủ năng lực để tham gia các chương trình học tập quốc tế hay không": "pointlookup",
            "Tôi muốn xem điểm số để biết mình đã đạt được các tiêu chí đánh giá của các tổ chức đánh giá năng lực hay chưa": "pointlookup"


        }

        most_similar = determine_most_similar_phrase(text, phrases)
        return phrases[most_similar]

    def point(self):

        with open('samples/rp_pl.json',encoding='utf-8') as f:
            data = json.load(f)
            self.questions = data.get('', [])
        question = random.choice(self.questions)
        speaker.speak(question)
   
 
        # Khởi tạo trình duyệt
        driver = webdriver.Edge()

        # Truy cập vào trang web
        driver.get("https://camau.bdu.edu.vn/tracuudiem/index.php")

        # # Khởi tạo đối tượng nhận dạng giọng nói
        # recognizer = sr.Recognizer()
        # microphone = sr.Microphone()

        # Yêu cầu người dùng nhập mã số sinh viên bằng giọng nói
        speaker.speak("Vui lòng nói mã số sinh viên")
        # with microphone as source:
        #     recognizer.adjust_for_ambient_noise(source)
        #     audio = recognizer.listen(source, timeout=3)

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
                    # with microphone as source:
                    #     recognizer.adjust_for_ambient_noise(source)
                    #     audio = recognizer.listen(source, timeout=3)

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
                        remember_checkbox = driver.find_element(By.NAME, "remember")
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

        # Lưu dữ liệu vào file excel
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
