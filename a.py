from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytesseract
from PIL import Image
import schedule
import time

# Đường dẫn tới thư mục cài đặt tesseract (có thể thay đổi nếu không phải là mặc định)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Cập nhật đúng đường dẫn Tesseract của bạn

# Khởi tạo trình duyệt
def start_browser():
    options = webdriver.ChromeOptions()
    # Tắt chế độ headless để có thể nhìn thấy trình duyệt
    # options.add_argument("--headless")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

# Lấy mã captcha và giải mã
def get_captcha(driver):
    try:
        captcha_image = driver.find_element(By.ID, "captchaImage")
        captcha_image.screenshot("captcha.png")  # Lưu ảnh captcha
        image = Image.open("captcha.png")
        captcha_text = pytesseract.image_to_string(image)  # Giải mã captcha
        return captcha_text.strip()
    except Exception as e:
        print(f"Không thể lấy mã captcha: {e}")
        return None

# Kiểm tra phạt nguội
def check_fine(license_plate, vehicle_type):
    driver = start_browser()

    try:
        # Mở trang web CSGT
        driver.get("https://www.csgt.vn/tra-cuu-phuong-tien-vi-pham.htm")
        
        # Đợi cho trang web tải xong và hiển thị các phần tử cần thiết
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "bienSoXe")))

        # Nhập biển số xe và chọn loại phương tiện
        driver.find_element(By.ID, "bienSoXe").send_keys(license_plate)
        driver.find_element(By.ID, "loaiPhuongTien").send_keys(vehicle_type)

        # Lấy mã captcha và nhập vào ô captcha
        captcha_text = get_captcha(driver)
        if captcha_text:
            driver.find_element(By.ID, "captchaInput").send_keys(captcha_text)

        # Nhấn nút tìm kiếm
        driver.find_element(By.ID, "btnSearch").click()

        # Đợi kết quả và kiểm tra phạt nguội
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "result")))
        result = driver.find_element(By.CLASS_NAME, "result")
        print(f"Phạt nguội: {result.text}")

    except Exception as e:
        print(f"Đã xảy ra lỗi khi kiểm tra phạt nguội: {e}")
    
    finally:
        driver.quit()

# Lên lịch chạy tự động
def job():
    print("Đang kiểm tra phạt nguội...")
    check_fine("29A-12345", "Ô tô")  # Thay "29A-12345" và "Ô tô" bằng thông tin phương tiện của bạn

# Thiết lập lịch trình chạy mỗi ngày lúc 6:00 AM và 12:00 PM
schedule.every().day.at("22:43").do(job)
schedule.every().day.at("12:00").do(job)

# Chạy lịch trình
while True:
    schedule.run_pending()
    time.sleep(1)
