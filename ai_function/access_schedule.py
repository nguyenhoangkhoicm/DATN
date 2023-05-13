from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime
from ai_function.determine_most_similar import determine_most_similar_phrase
from ai_function.speaklisten import speaker
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import subprocess,os,re,time,json,random

class schedule():
    def main(self, text, intent):
        task = self.determine_search_or_open(text)
        if task == 'schedule':
            self.access_schedule()

    def determine_search_or_open(self, text):
        phrases = {
            'Bạn xem giúp mình lịch học với': 'schedule',
            'Bạn có thể xem giúp mình lịch học được không':'schedule',
            'Bạn giúp mình xem lịch học được không':'schedule',
            'Bạn có thể kiểm tra lịch học cho mình được không':'schedule',
            'Bạn giúp mình kiểm tra lịch học được không':'schedule',
            'Bạn có thể xem giúp mình lịch học với':'schedule',
            'Bạn có thể kiểm tra giúp mình lịch học được không':'schedule',
            'Bạn có thể xem giúp mình lịch học được chứ':'schedule',
           ' Bạn giúp mình xem lịch học được chứ':'schedule'
        }
        most_similar = determine_most_similar_phrase(text, phrases)
        return phrases[most_similar]

    def access_schedule(self):

        with open('samples/access_schedule.json',encoding='utf-8') as f:
            data = json.load(f)
            questions= data.get('', [])
        question = random.choice(questions)
        speaker.speak(question)

        url = "https://camau.bdu.edu.vn/sinh-vien"
        # Mở trang web
        driver = webdriver.Edge()
        driver.get(url)

        wait = WebDriverWait(driver, 10)
        schedule_elements = wait.until(EC.presence_of_all_elements_located(
            (By.XPATH, "//a[contains(@href, '/sinh-vien/')]")))
        
        # latest_schedule_link = None
        # latest_date = datetime.min

        # for element in schedule_elements:
        #     link_text = element.text
        #     date_match = re.search(r'\d{2}/\d{2}/\d{4}', link_text)
        #     if date_match:
        #         date_str = date_match.group()
        #         date_obj = datetime.strptime(date_str, '%d/%m/%Y')
        #         if date_obj > latest_date:
        #             latest_date = date_obj
        #             latest_schedule_link = element
        latest_schedule_link = None
        latest_date = None

        for element in schedule_elements:
            link_text = element.text
            date_match = re.search(r'\d{2}/\d{2}/\d{4}', link_text)
            if date_match:
                date_str = date_match.group()
                date_obj = datetime.strptime(date_str, '%d/%m/%Y')
                if latest_date is None or date_obj > latest_date:
                    latest_date = date_obj
                    latest_schedule_link = element

        if latest_schedule_link:

            # tìm kiếm lịch học mới nhất
            latest_schedule_link.click()

            pdf_link = wait.until(EC.presence_of_element_located(
                (By.XPATH, "//p[contains(., 'Xem lịch học tại đây')]/following-sibling::p//img")))
            pdf_link.click()

            # Xác định đường dẫn đến thư mục tải xuống
            download_folder = os.path.expanduser("~") + "/Downloads/"

            # Lấy thời gian hiện tại
            start_time = time.time()

            # Tên tệp PDF
            pdf_file = ''

            # Tải tệp PDF về máy
            download_button = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@aria-label='Tải xuống']")))
            download_button.click()

            # Chờ đợi tệp PDF được tải xuống và lưu trữ tên tệp
            while True:
                # Lấy danh sách tệp trong thư mục tải xuống
                files = os.listdir(download_folder)

                # Lọc các tệp PDF
                pdf_files = [f for f in files if f.endswith(".pdf")]

                # Kiểm tra xem có tệp PDF mới tải xuống hay không
                if len(pdf_files) > 0:
                    # Lấy tên tệp PDF mới nhất
                    pdf_file = pdf_files[-1]
                    # Kiểm tra xem tệp PDF đã được tải xuống hoàn tất hay chưa
                    if os.path.getsize(download_folder + pdf_file) > 0:
                        break
                    else:
                        time.sleep(1)
                else:
                    time.sleep(1)

                # Kiểm tra xem đã vượt quá thời gian chờ tối đa hay chưa
                if time.time() - start_time > 60:
                    break

            # Kiểm tra xem tệp PDF đã tải xuống thành công hay không
            if pdf_file != '':
                # Mở tệp PDF bằng trình xem PDF mặc định
                subprocess.Popen([download_folder + pdf_file], shell=True)
            else:
                speaker.speak("Không tìm thấy tệp PDF tải xuống!")

            with open('samples/result_access_schedule.json',encoding='utf-8') as f:
                data = json.load(f)
                questions= data.get('', [])
            question = random.choice(questions)
            speaker.speak(question)
    
schedule = schedule()
