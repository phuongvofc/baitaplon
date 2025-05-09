import time
import pytesseract
from PIL import Image
import requests
from io import BytesIO
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import schedule

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

BIEN_SO = "30A12345"
LOAI_PHUONG_TIEN = "Ô tô"

def check_fines():
    options = Options()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        driver.get("https://www.csgt.vn/tra-cuu-phuong-tien-vi-pham.htm")

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "code")))
        driver.find_element(By.ID, "code").send_keys(BIEN_SO)

        Select(driver.find_element(By.ID, "vehicleType")).select_by_visible_text(LOAI_PHUONG_TIEN)

        captcha_src = driver.find_element(By.ID, "captchaimg").get_attribute("src")
        img_bytes = requests.get(captcha_src).content
        img = Image.open(BytesIO(img_bytes))
        captcha_text = pytesseract.image_to_string(img, config='--psm 8').strip()
        captcha_text = ''.join(filter(str.isalnum, captcha_text))[:6]

        driver.find_element(By.ID, "id_captcha_code").send_keys(captcha_text)
        driver.find_element(By.XPATH, "//button[contains(text(),'Tra cứu')]").click()

        time.sleep(3)
        if "không tìm thấy kết quả" in driver.page_source.lower():
            print("Không có kết quả phạt nguội.")
        else:
            print("Có thể có kết quả phạt nguội.")

    except Exception as e:
        print("Lỗi:", e)

    finally:
        driver.quit()

schedule.every().day.at("06:00").do(check_fines)
schedule.every().day.at("12:00").do(check_fines)

print("Đang chạy nền...")

while True:
    schedule.run_pending()
    time.sleep(1)
