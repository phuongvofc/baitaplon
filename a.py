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

# Đường dẫn tới tesseract OCR trên máy
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

BIEN_SO = "30A12345"               # <-- Thay biển số xe thật ở đây
LOAI_PHUONG_TIEN = "Ô tô"          # "Ô tô" hoặc "Xe máy"

def check_fines():
    print(">>> Bắt đầu kiểm tra phạt nguội...\n")
    
    options = Options()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    options.add_argument("--headless")  # chạy ẩn trình duyệt (nếu muốn hiển thị thì xóa dòng này)
    options.add_argument("--disable-gpu")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        driver.get("https://www.csgt.vn/tra-cuu-phuong-tien-vi-pham.html")

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "code")))
        driver.find_element(By.ID, "code").send_keys(BIEN_SO)

        select = Select(driver.find_element(By.ID, "vehicleType"))
        select.select_by_visible_text(LOAI_PHUONG_TIEN)

        # Lấy ảnh captcha
        captcha_img = driver.find_element(By.ID, "captchaimg")
        src = captcha_img.get_attribute("src")
        img_bytes = requests.get(src).content
        img = Image.open(BytesIO(img_bytes))

        # Giải mã captcha
        captcha_text = pytesseract.image_to_string(img, config='--psm 8').strip()
        captcha_text = ''.join(filter(str.isalnum, captcha_text))[:6]
        print("Giải mã Captcha:", captcha_text)

        driver.find_element(By.ID, "id_captcha_code").send_keys(captcha_text)
        driver.find_element(By.XPATH, "//button[contains(text(),'Tra cứu')]").click()

        time.sleep(3)
        page_source = driver.page_source.lower()

        if "không tìm thấy kết quả" in page_source:
            print("✅ Không có phạt nguội.\n")
        else:
            print("⚠️ CÓ THỂ có kết quả phạt nguội. Kiểm tra lại trang web!\n")

    except Exception as e:
        print("❌ Lỗi khi kiểm tra phạt nguội:", e)

    finally:
        driver.quit()

# Lên lịch chạy lúc 6h sáng và 12h trưa mỗi ngày
schedule.every().day.at("06:00").do(check_fines)
schedule.every().day.at("12:00").do(check_fines)

print("⏰ Đang chờ đến 06:00 và 12:00 để tự động kiểm tra...")

# Vòng lặp chạy mãi
while True:
    schedule.run_pending()
    time.sleep(1)
