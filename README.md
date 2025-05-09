
# Project Title

A brief description of what this project does and who it's for

# Dự án Kiểm Tra Phạt Nguội

Dự án này sử dụng Python và Selenium để tự động kiểm tra phạt nguội phương tiện giao thông từ trang web CSGT (https://www.csgt.vn/tra-cuu-phuong-tien-vi-pham.htm).

## Các tính năng:
- Nhập biển số xe và loại phương tiện.
- Tự động lấy mã captcha từ trang web và giải mã bằng Tesseract OCR.
- Kiểm tra và hiển thị kết quả phạt nguội.
- Lên lịch kiểm tra phạt nguội mỗi ngày vào lúc 6:00 AM và 12:00 PM.

## Yêu cầu:
Để chạy dự án này, bạn cần cài đặt các thư viện sau:

- `selenium`
- `webdriver-manager`
- `pytesseract`
- `pillow`
- `schedule`

## Cài đặt:
1. Cài đặt Python (phiên bản 3.6 trở lên) từ [Python Official Site](https://www.python.org/downloads/).
2. Cài đặt các thư viện yêu cầu bằng cách sử dụng pip:
   ```bash
   pip install -r requirements.txt
