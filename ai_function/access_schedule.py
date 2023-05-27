from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from ai_function.determine_most_similar import determine_most_similar_phrase
from ai_function.speaklisten import speaker
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import subprocess
import os
import time
import json
import random


class schedule():
    def main(self, text, intent):
        task = self.determine_search_or_open(text)
        if task == 'schedule':
            self.access_schedule()

    def determine_search_or_open(self, text):
        phrases = {
            'Bạn xem giúp mình lịch học với': 'schedule',
            'Bạn có thể xem giúp mình lịch học được không': 'schedule',
            'Bạn giúp mình xem lịch học được không': 'schedule',
            'Bạn có thể kiểm tra lịch học cho mình được không': 'schedule',
            'Bạn giúp mình kiểm tra lịch học được không': 'schedule',
            'Bạn có thể xem giúp mình lịch học với': 'schedule',
            'Bạn có thể kiểm tra giúp mình lịch học được không': 'schedule',
            'Bạn có thể xem giúp mình lịch học được chứ': 'schedule',
            'Bạn giúp mình xem lịch học được chứ': 'schedule',
            'Bạn có thể cho tôi xem lịch học được không': 'schedule',
            'Tôi cần kiểm tra lịch học của mình, có thể xem giúp tôi': 'schedule',
            'Tôi không nhớ lịch học của mình, bạn có thể cho tôi xem lại được không': 'schedule',
            'Bạn có thể gửi cho tôi lịch học của mình qua email được không': 'schedule',
            'Tôi cần xem lịch học để có thể sắp xếp thời gian làm việc của mình': 'schedule',
            'Tôi muốn biết lịch học của mình để có thể chuẩn bị tốt cho các bài kiểm tra và bài tập': 'schedule',
            'Tôi đang có rắc rối với lịch học của mình, bạn có thể giúp tôi xem lại được không': 'schedule',
            'Tôi đang muốnkiểm tra lịch học của mình để tiện cho việc sắp xếp thời gian đi học': 'schedule',
            'Tôi cần xem lịch học để biết được thời gian của các buổi học và đảm bảo không bỏ sót bất kỳ buổi nào': 'schedule',
            'Bạn có thể cho tôi biết lịch học của mình để tôi có thể chuẩn bị trước cho các bài giảng, bài tập': 'schedule',
            'Tôi cần xem lịch học để biết thời gian của các buổi học và đảm bảo không bị trùng lịch với các hoạt động khác': 'schedule',
            'Tôi muốn xem lịch học để biết được thời gian của các buổi học và chuẩn bị trước cho các bài tập': 'schedule',
            'Tôi cần xem lịch học để biết thời gian của các buổi học và có thể sắp xếp thời gian học tập cho phù hợp': 'schedule',
            'Bạn có thể cho tôi xem lịch học để tôi có thể đăng ký các hoạt động ngoại khóa phù hợp': 'schedule',
            'Tôi cần xem lịch học để biết thời gian của các buổi học và có thể sắp xếp lịch làm việc của mình': 'schedule',
            'Tôi muốn xem lịch học để biết thời gian của các buổi học và có thể điều chỉnh các kế hoạch cá nhân của mình': 'schedule',
            'Tôi cần xem lịch học để biết thời gian của các buổi học và đảm bảo tham gia đầy đủ các buổi học': 'schedule',
            'Tôi muốn xem lịch học để biết thời gian của các buổi học và có thể sắp xếp thời gian học tập cho phù hợp với lịch trình của mình': 'schedule',
            'Tôi cần xem lịch học để biết thời gian của các buổi học và đảm bảo không bỏ lỡ bất kỳ buổi nào': 'schedule',
            'Bạn có thể cho tôi xem lịch học để tôi có thể sắp xếp thời gian làm việc và học tập hợp lý': 'schedule',
            'Tôi muốn xem lịch học để biết thời gian của các buổi học và có thể sắp xếp thời gian đi lại phù hợp': 'schedule',
            'Tôi cần xem lịch học để biết thời gian của các buổi học và có thể đảm bảo tham gia đầy đủ các hoạt động học tập': 'schedule',
            'Tôi muốn xem lịch học để biết thời gian của các buổi học và có thể sắp xếp thời gian học tập cho phù hợp với các môn học khác': 'schedule',
            'Tôi cần xem lịch học để biết thời gian của các buổi học và có thể sắp xếp thời gian học tập cho phù hợp với lịch trình làm việc của mình': 'schedule',
            'Bạn có thể giúp tôi kiểm tra lịch học của mình để tôi có thể sắp xếp thời gian đi học và đi lại phù hợp': 'schedule',
            'Tôi muốn xem lịch học để biết thời gian của các buổi học và có thể sắp xếp thời gian học tập cho phù hợp với các hoạt động khác': 'schedule',
            'Tôi cần xem lịch học để biết thời gian của các buổi học và có thể chuẩn bị trước cho các bài kiểm tra và bài tập': 'schedule',
            'Tôi muốn kiểm tra lịch học của mình để biết thời gian của các buổi học và có thể xem xét thời gian cho các hoạt động ngoại khóa khác': 'schedule',
            'Tôi cần xem lịch học để biết thời gian của các buổi học và có thể sắp xếp thời gian học tập cho phù hợp với các môn học khác trong cùng kỳ học': 'schedule',
            'Bạn có thể cho tôi xem lịch học để tôi có thể sắp xếp thời gian học tập cho phù hợp với lịch trình cá nhân': 'schedule',
            'Tôi muốn kiểm tra lịch học của mình để biết thời gian của các buổi học và có thể sắp xếp thời gian làm việc khác phù hợp': 'schedule',
            'Tôi cần xem lịch học để biết thời gian của các buổi học và có thể sắp xếp thời gian đi lại phù hợp với lịch trình học tập': 'schedule',
            'Tôi muốn xem lịch học để biết thời gian của các buổi học và có thể sắp xếp thời gian cho các hoạt động tập thể khác': 'schedule',
            'Tôicần xem lịch học để biết thời gian của các buổi học và có thể sắp xếp thời gian học tập cho phù hợp với các kế hoạch dài hạn của mình': 'schedule',
            'Bạn có thể giúp tôi xem lại lịch học để tôi có thể đảm bảo không bị trùng lịch với các hoạt động khác': 'schedule',
            'Tôi muốn xem lịch học để biết thời gian của các buổi học và có thể sắp xếp thời gian đi học cho phù hợp với lịch trình của mình': 'schedule',
            'Tôi cần xem lịch học để biết thời gian của các buổi học và có thể sắp xếp thời gian học tập cho phù hợp với lịch trình cá nhân của mình': 'schedule',
            'Tôi muốn xem lịch học để biết thời gian của các buổi học và có thể đăng ký các lớp học thêm phù hợp': 'schedule',
            'Tôi cần xem lịch học để biết thời gian của các buổi học và có thể sắp xếp thời gian đi lại cho phù hợp với lịch trình học tập của mình': 'schedule',
            'Tôi muốn kiểm tra lịch học của mình để đảm bảo không bỏ lỡ bất kỳ buổi học hay các hoạt động học tập nào': 'schedule',
            'Tôi cần xem lịch học để biết thời gian của các buổi học và có thể sắp xếp thời gian học tập cho phù hợp với các kế hoạch du lịch': 'schedule',
            'Tôi muốn xem lịch học để biết thời gian của các buổi học và có thể sắp xếp thờigian học tập cho phù hợp với lịch trình công việc của mình': 'schedule',
            'Tôi cần xem lịch học để biết thời gian của các buổi học và có thể sắp xếp thời gian học tập cho phù hợp với các hoạt động tình nguyện': 'schedule',
            'Tôi muốn kiểm tra lịch học của mình để đảm bảo có đủ thời gian cho các hoạt động giải trí và thư giãn': 'schedule',
            'Tôi cần xem lịch học để biết thời gian của các buổi học và có thể sắp xếp thời gian học tập cho phù hợp với các hoạt động thể thao': 'schedule',
            'Tôi muốn xem lịch học để biết thời gian của các buổi học và có thể sắp xếp thời gian học tập cho phù hợp với sở thích cá nhân': 'schedule',
            'Tôi cần xem lịch học để biết thời gian của các buổi học và có thể chuẩn bị tốt hơn cho các bài kiểm tra và bài tập': 'schedule',
            'Tôi muốn xem lịch học để biết thời gian của các buổi học và có thể sắp xếp thời gian học tập cho phù hợp với lịch trình làm việc của mình': 'schedule',
            'Tôi cần xem lịch học để biết thời gian của các buổi học và có thể đảm bảo tham gia đầy đủ các hoạt động học tập': 'schedule',
            'Tôi muốn xem lịch học để biết thời gian của các buổi học và có thể đăng ký các khóa học trực tuyến phù hợp với lịch trình của mình': 'schedule',
            'Lịch học của tôi sẽ được đăng tải ở đâu': 'schedule',
            'Khi nào lịch học của học kỳ mới sẽ được công bố': 'schedule',
            'Làm thế nào để biết lịch học của mình': 'schedule',
            'Tôi có thể xem lịch học trực tuyến hay không': 'schedule',
            'Lịch học của tôi sẽ được gửi về địa chỉ email của tôi hay không': 'schedule',
            'Tôi có thể yêu cầu in lịch học của mình tại văn phòng trường không': 'schedule',
            'Tôi có thể xem lịch học của các môn học trên một trang web riêng không': 'schedule',
            'Tôi có thể xem lịch học của các môn học trên ứng dụng trên điện thoại không': 'schedule',
            'Tôi có thể xem lịch học chi tiết củatừng môn học không': 'schedule',
            'Tôi có thể yêu cầu chuyển lịch học của mình qua email hay không': 'schedule',
            'Lịch học sẽ được cập nhật đầy đủ và chính xác không': 'schedule',
            'Tôi cần phải đăng nhập vào hệ thống nào để xem lịch học của mình': 'schedule',
            'Tôi cần phải làm thủ tục gì để xem lịch học': 'schedule',
            'Tôi có thể xem lại lịch học của học kỳ trước không': 'schedule',
            'Tôi có thể yêu cầu in lại lịch học của mình không': 'schedule',
            'Tôi có thể yêu cầu xem lịch học của các môn học mà tôi đã bỏ thi không': 'schedule',
            'Tôi có thể yêu cầu xem lịch học của các môn học mà tôi đã trượt không': 'schedule',
            'Tôi có thể xem lịch học của các môn học đã học trong học kỳ trước không': 'schedule',
            'Tôi có thể đưa ra yêu cầu thay đổi lịch học nếu có vấn đề gì không': 'schedule',
            'Tôi có thể xem lịch học của các môn học trung bình không': 'schedule',
            'Tôi có thể xem lịch học của các môn học theo thứ tự môn học không': 'schedule',
            'Tôi có thể xem lịch học của các môn học theo thứ tự giảng viên không': 'schedule',
            'Tôi có thể xem lịch học của các môn học theo thứ tự mã số môn học không': 'schedule',
            'Tôi có thể xem lịch học của các môn học theo thứ tự số tín chỉ không': 'schedule',
            'Tôi có thể xem lịch học của các môn học theo thứ tự học kỳ không': 'schedule',
            'Tôi có thể yêu cầu xem lịch học của các môn học đang học trong học kỳ hiện tại không': 'schedule',
            'Tôi có thể yêu cầu xem lịch học của các môn học đã hoàn thành trong học kỳ hiện tại không': 'schedule',
            'Tôi có thể yêu cầu xem lịch học của các môn học đã học trong học kỳ trước không': 'schedule',
            'Tôi có thể xem lịch học của mình trên ứng dụng di động không': 'schedule',
            'Tôi có thể yêu cầu in lịch học của mình qua bưu điện hay không': 'schedule',
            'Tôi có thể yêu cầu nhận lịch học của mình qua email hay không': 'schedule',
            'Tôi có thể yêu cầu nhận lịch học của mình qua tin nhắn SMS hay không': 'schedule',
            'Tôi có thể yêu cầu gửi lịch học của mình đến địa chỉ khác không': 'schedule',
            'Tôi có thể yêu cầu tổng hợp lịch học của mình theo từng học kỳ không': 'schedule',
            'Tôi có thể yêu cầu tổng hợp lịch học của mình theo từng năm học không': 'schedule',
            'Tôi có thể xem lịch học của các môn học theo thứtự số thứ tự không': 'schedule',
            'Tôi có thể xem lịch học của các môn học theo thứ tự số phòng học không': 'schedule',
            'Tôi có thể xem lịch học của các môn học theo thứ tự thời gian học không': 'schedule',
            'Tôi có thể xem lịch học của các môn học theo thứ tự giờ học không': 'schedule',
            'Tôi có thể xem lịch học của các môn học theo thứ tự ngày học không': 'schedule',
            'Tôi có thể xem lịch học của các môn học tại trung tâm học thuật không': 'schedule',
            'Tôi có thể xem lịch học của các môn học tại khoa khoa học và công nghệ không': 'schedule',
            'Tôi có thể xem lịch học của các môn học tại khoa kinh tế và quản lý không': 'schedule',
            'Tôi có thể xem lịch học của các môn học tại khoa y khoa không': 'schedule',
            'Tôi có thể xem lịch học của các môn học tại khoa sư phạm không': 'schedule',
            'Tôi có thể xem lịch học của các môn học tại khoa luật không': 'schedule',
            'Tôi có thể xem lịch học của các môn học tại khoa ngoại ngữ không': 'schedule',
            'Tôi có thể xem lịch học của các môn học tại khoa truyền thông và đa phương tiện không': 'schedule',
            'Tôi có thể xem lịch học của các môn học tại khoa kỹ thuật công nghệ không': 'schedule',
            'Tôi có thể xem lịch học của các môn học tại khoa khoa học xã hội và nhân văn không': 'schedule',
            'Tôi có thể xem lịch học của các môn học tại khoa khoa học máy tính không': 'schedule',
            'Tôi có thể xem lịch học của các môn học tại khoa khoa học tự nhiên không': 'schedule',
            'Tôi có thể xem lịch học của các môn học tại khoa đào tạo quốc tế không': 'schedule',
            'Tôi có thể xem lịch học của các môn học tại khoa nghiên cứu khoa học và công nghệ không': 'schedule',
            'Tôi có thể xem lịch học của các môn học tại trung tâm đào tạo phát triển cá nhân không': 'schedule',
            'Tôi có thể xem lịch học của các môn học tại trung tâm giáo dục quốc phòng và an ninh không': 'schedule',
            'Tôi có thể xem lịch học của các môn học tại trung tâm nghiên cứu và ứng dụng khoa học không': 'schedule',
            'Lịch học của tôi có thể bị thay đổi không': 'schedule',
            'Tôi cần phải kiểm tra lịch học của mình thường xuyên không': 'schedule',
            'Lịch học của tôi có thể bị hủy không': 'schedule',
            'Tôi có thể yêu cầu thay đổi lịch học của mình nếu có lý do khẩn cấp không': 'schedule',
            'Tôi cần phải báo trước bao nhiêu ngày nếu muốn thay đổi lịch học': 'schedule',
            'Tôi có thể yêu cầu thay đổi lịch học của mình nếu có môn học trùng lịch không': 'schedule',
            'Tôi có thể yêu cầu thay đổi lịch học của mình nếu có xung đột lịch với các hoạt động khác không': 'schedule',
            'Tôi cần phải liên hệ với ai để thay đổi lịch học của mình': 'schedule',
            'Tôi có thể yêu cầu thay đổi lịch học của mình nếu có giảng viên không dạy được không': 'schedule',
            'Tôi có thể yêu cầu thay đổi lịch học của mình nếu có giảng viên bận việc riêng không': 'schedule',
            'Tôi có thể yêu cầu thay đổi lịch học của mình nếu có sự kiện đặc biệt trong trường không': 'schedule',
            'Tôi có thể yêu cầu thay đổi lịch học của mình nếu có khóa học hợp lí hơn không': 'schedule',
            'Tôi có thể yêu cầu thay đổi lịch học của mình nếu có sự cố về thiết bị không': 'schedule',
            'Tôi có thể yêu cầu thay đổi lịch học của mình nếu có thay đổi trong chương trình giảng dạy không': 'schedule',
            'Tôi có thể yêu cầu thay đổi lịch học của mình nếu có thay đổi trong giảng viên không': 'schedule',
            'Tôi có thể yêu cầu thay đổi lịch học của mình nếu có thay đổi về phòng học không': 'schedule',
            'Tôi có thể yêu cầu thay đổi lịch học của mình nếu có tình huống khẩn cấp không': 'schedule',
            'Tôi cần phải làm thủ tục gì để yêu cầu thay đổi lịch học': 'schedule',
            'Tôicần phải nộp đơn yêu cầu thay đổi lịch học hay không': 'schedule',
            'Tôi cần phải giải thích lý do thay đổi lịch học khi yêu cầu thay đổi không': 'schedule',
            'Tôi cần phải nêu rõ các thông tin cụ thể khi yêu cầu thay đổi lịch học': 'schedule',
            'Tôi cần phải đối chiếu lịch học mới với lịch học cũ trước khi yêu cầu thay đổi không': 'schedule',
            'Tôi cần phải chờ bao lâu để biết kết quả yêu cầu thay đổi lịch học': 'schedule',
            'Tôi có thể yêu cầu thay đổi lịch học nhiều lần trong một học kỳ không': 'schedule',
            'Tôi cần phải làm thủ tục gì để hủy lịch học': 'schedule',
            'Tôi cần phải báo trước bao nhiêu ngày khi muốn hủy lịch học': 'schedule',
            'Tôi cần phải có lý do gì đểhủy lịch học': 'schedule',
            'Tôi có thể hủy lịch học trực tiếp tại phòng đăng ký học phần không': 'schedule',
            'Tôi có thể hủy lịch học qua email hay không': 'schedule',
            'Tôi có thể hủy lịch học qua điện thoại hay không': 'schedule',
            'Tôi cần phải làm thủ tục gì để đổi phòng học': 'schedule',
            'Tôi có thể đổi phòng học trong cùng một ngày học không': 'schedule',
            'Tôi có thể đổi phòng học trong cùng một tuần học không': 'schedule',
            'Tôi cần phải báo trước bao nhiêu ngày khi muốn đổi phòng học': 'schedule',
            'Tôi cần phải có lý do gì để đổi phòng học': 'schedule',
            'Tôi có thể đổi phòng học trực tiếp tại phòng đăng ký học phần không': 'schedule',
            'Tôi có thể đổi phòng học qua email hay không': 'schedule',
            'Tôi có thể đổi phòng học qua điện thoại hay không': 'schedule',
            'Tôicần phải liên hệ với ai để yêu cầu đổi phòng học': 'schedule',
            'Tôi có thể yêu cầu đổi phòng học nếu phòng học cũ không phù hợp không': 'schedule',
            'Tôi có thể yêu cầu đổi phòng học nếu có sự cố về thiết bị trong phòng học không': 'schedule',
            'Tôi có thể yêu cầu đổi phòng học nếu có yêu cầu đặc biệt trong môn học không': 'schedule'

        }
        most_similar = determine_most_similar_phrase(text, phrases)
        return phrases[most_similar]

    def access_schedule(self):

        with open('samples/access_schedule.json', encoding='utf-8') as f:
            data = json.load(f)
            questions = data.get('', [])
        question = random.choice(questions)
        speaker.speak(question)

        edge_options = Options()
        edge_options.add_argument("--incognito")

        url = "https://camau.bdu.edu.vn/sinh-vien"

        try:
            # Mở trang web
            driver = webdriver.Edge(options=edge_options)
            driver.get(url)

            wait = WebDriverWait(driver, 10)

            latest_schedule = wait.until(EC.presence_of_element_located(
                (By.XPATH, "//h5[contains(text(),'Lịch học tuần')]")))
            latest_schedule.click()

            pdf_link = wait.until(EC.presence_of_element_located(
                (By.XPATH, "//p[contains(., 'Xem lịch học tại đây')]/following-sibling::p//img")))
            pdf_link.click()

            download_folder = os.path.expanduser("~") + "/Downloads/"

            start_time = time.time()

            while True:
                files = os.listdir(download_folder)
                pdf_files = [f for f in files if f.endswith(".pdf")]

                if len(pdf_files) > 0:
                    pdf_file = pdf_files[-1]
                    if os.path.getsize(download_folder + pdf_file) > 0:
                        break
                    else:
                        time.sleep(1)
                else:
                    time.sleep(1)

                if time.time() - start_time > 60:
                    raise Exception(
                        "Tệp PDF không được tải xuống trong thời gian cho phép.")

            subprocess.Popen([download_folder + pdf_file], shell=True)

            with open('samples/result_access_schedule.json', encoding='utf-8') as f:
                data = json.load(f)
                questions = data.get('', [])
            question = random.choice(questions)
            speaker.speak(question)

        except Exception as e:
            speaker.speak(str(e))

        finally:
            driver.quit()


schedule = schedule()
