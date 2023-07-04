from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import subprocess
import os
import time
import json
import random

from ai_function.determine_most_similar import determine_most_similar_phrase
from ai_function.speaklisten import speaker


class schedule():
    def main(self, text, intent):
        task = self.determine_search_or_open(text)
        if task == 'schedule':
            self.access_schedule()

    def determine_search_or_open(self, text):
        with open('samples/phrases_access.json', 'r', encoding='utf-8') as file:
            phrases = json.load(file)
        most_similar = determine_most_similar_phrase(text, phrases)
        return phrases[most_similar]

    def access_schedule(self):

        # with open('samples/access_schedule.json', encoding='utf-8') as f:
        #     data = json.load(f)
        #     questions = data.get('', [])
        # question = random.choice(questions)
        # speaker.speak(question)

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

            download_button = wait.until(EC.presence_of_element_located(
                    (By.XPATH, "/html/body/div[3]/div[4]/div/div[3]/div[2]/div[2]/div[3]")))
            download_button.click()
            
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
