# 📚 [LAB 2] APPLICATION PROGRAMMING INTERFACE AND FIREBASE STUDIO

---

## 🧑‍💻 Thông tin sinh viên
| Hạng mục | Chi tiết |
| :--- | :--- |
| **Họ và tên** | Huỳnh Huy Hoàng |
| **Mã số sinh viên** | 24120181 |
| **Lớp** | 24CTT5 |
| **Trường** | Đại học Khoa học Tự nhiên - ĐHQG-HCM |
| **Môn học** | Tư duy tính toán |
| **Giảng viên** | Lê Đức Khoan |

---

## 📖 Tổng quan dự án
* Bài Lab này tập trung vào việc xây dựng một ứng dụng hoàn chỉnh với sự tách biệt rõ ràng giữa **Frontend** và **Backend**.
* Hệ thống sử dụng **FastAPI** để xây dựng API , **Firebase** để xác thực người dùng và lưu trữ dữ liệu, kết hợp với mô hình **AI (Image Classification)** để thực hiện tính năng chính.

### 🛠 Công nghệ sử dụng
* **Backend:** FastAPI (Python), Firebase Admin SDK.
* **Frontend:** Streamlit.
* **Database & Auth:** Firebase Authentication & Firestore Database.
* **AI Model:** Transformers (Hugging Face) - Image Classification.

---

## ✨ Các tính năng chính
Ứng dụng cung cấp các chức năng cốt lõi theo yêu cầu của bài Lab:

### 1. Hệ thống xác thực (Authentication)
* **Đăng ký:** Tạo tài khoản mới trực tiếp trên giao diện.
* **Đăng nhập:** Linh hoạt qua Email/Password hoặc sử dụng UID.
* **Quản lý:** Nhận diện thông tin người dùng hiện tại và chức năng Đăng xuất.

### 2. Nhận diện hình ảnh (Feature chính) 
* **Tải ảnh:** Người dùng tải ảnh lên từ máy tính qua Frontend.
* **Ghi chú:** Nhập ghi chú cá nhân kèm theo mỗi bức ảnh để lưu trữ ngữ cảnh.
* **Phân tích:** Hệ thống tự động phân tích và trả về kết quả nhận diện đối tượng thực tế qua Backend.

### 3. Quản lý dữ liệu (Database operations) 
* **Lưu trữ:** Tự động lưu lịch sử nhận diện và ghi chú vào Firestore.
* **Truy xuất:** Hiển thị danh sách lịch sử chi tiết cho từng người dùng.
* **Trực quan:** Cung cấp biểu đồ thống kê các loại ảnh đã thực hiện phân tích.

---

## 📂 Cấu trúc thư mục dự án 
```plaintext
project/
├── backend/                # Chứa mã nguồn xử lý logic API
│   ├── main.py             # File chạy chính của FastAPI
│   └── serviceAccountKey.json # Private key kết nối Firebase (Đã ẩn)
├── frontend/               # Chứa mã nguồn giao diện người dùng
│   └── app.py              # File chạy chính của Streamlit 
├── .gitignore              # Loại bỏ các file bí mật và bộ nhớ tạm 
├── requirements.txt        # Danh sách các thư viện cần cài đặt 
└── README.md               # Hướng dẫn chi tiết dự án 
```
---

## 🚀 Hướng dẫn cài đặt và khởi chạy   

### 1. Cài đặt môi trường
Tại thư mục gốc của dự án, chạy lệnh:
Bash
``` 
pip install -r requirements.txt
```
### 2. Khởi chạy Backend (FastAPI)
Mở terminal và di chuyển vào thư mục backend:
Bash
```
cd backend
python -m uvicorn main:app --reload
```

* Note: API sẽ hoạt động tại: http://127.0.0.1:8000 

### 3. Khởi chạy Frontend (Streamlit)
Mở một Terminal mới và di chuyển vào thư mục frontend:
Bash
```
cd frontend
python -m streamlit run app.py
```

* Note: Giao diện web sẽ tự động mở tại: http://localhost:8501   

## 📹 Video Demo ứng dụng   
Video trình bày đầy đủ quá trình vận hành hệ thống, từ đăng nhập đến thao tác dữ liệu thực tế trên Firebase.
# 🔗 [https://drive.google.com/drive/folders/1WwyWOiymXZP48JaqNQt3IKbZQrPbRH9i?usp=drive_link]