from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import firebase_admin
from firebase_admin import credentials, auth, firestore
from typing import List, Optional
from fastapi import File, UploadFile
import time
from fastapi import Form
from transformers import pipeline
from PIL import Image
import io
import requests 
import os
from dotenv import load_dotenv

# Tải các biến từ file .env
load_dotenv()

# Lấy API Key từ biến môi trường
FIREBASE_API_KEY = os.getenv("FIREBASE_API_KEY")

# Kiểm tra xem có lấy được key không 
if not FIREBASE_API_KEY:
    print("❌ Lỗi: Không tìm thấy FIREBASE_API_KEY trong file .env!")

app = FastAPI()

# Khởi tạo Firebase 
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# Sử dụng mô hình phân loại hình ảnh phổ biến của Google
pipe = pipeline("image-classification", model="google/vit-base-patch16-224")

# Định nghĩa Schema cho dữ liệu (Pydantic) 
class LoginRequest(BaseModel):
    email: Optional[str] = None
    password: Optional[str] = None
    uid: Optional[str] = None

class FeatureData(BaseModel):
    user_id: str
    content: str

class RegisterRequest(BaseModel):
    email: str
    password: str

# 1. Endpoint mặc định & Health Check 
@app.get("/")
async def root():
    return {"message": "API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# 2. Endpoint xác thực 
@app.post("/auth/login")
async def login(request: LoginRequest):
    # TRƯỜNG HỢP 1: Đăng nhập bằng UID 
    if request.uid:
        try:
            user = auth.get_user(request.uid)
            return {"status": "success", "uid": user.uid, "email": user.email}
        except:
            raise HTTPException(status_code=401, detail="UID không tồn tại")
    
    # TRƯỜNG HỢP 2: Đăng nhập bằng Email/Password 
    elif request.email and request.password:
        url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_API_KEY}"
        payload = {"email": request.email, "password": request.password, "returnSecureToken": True}
        res = requests.post(url, json=payload)
        if res.status_code == 200:
            data = res.json()
            return {"status": "success", "uid": data['localId'], "email": data['email']}
        else:
            raise HTTPException(status_code=401, detail="Sai Email hoặc Mật khẩu")
            
    raise HTTPException(status_code=400, detail="Thiếu thông tin đăng nhập")

@app.post("/auth/register")
async def register(request: RegisterRequest):
    try:
        # Sử dụng Firebase Admin SDK để tạo user mới
        user = auth.create_user(
            email=request.email,
            password=request.password
        )
        return {"status": "success", "uid": user.uid, "email": user.email}
    except Exception as e:
        # Trả về lỗi nếu email đã tồn tại hoặc định dạng không đúng
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/auth/me")
async def get_me(user_id: str):
    # Trả về thông tin người dùng từ DB hoặc Firebase Auth 
    try:
        user = auth.get_user(user_id)
        return {"uid": user.uid, "email": user.email}
    except Exception:
        raise HTTPException(status_code=404, detail="User not found")

# 3. Endpoint cho Feature chính & Database
@app.post("/detect")
async def detect_image(
    user_id: str = Form(...), 
    note: str = Form(None), # Nhận ghi chú từ người dùng
    file: UploadFile = File(...)
):
    try:
        #  Đọc file ảnh và chuyển sang định dạng PIL
        contents = await file.read()
        image = Image.open(io.BytesIO(contents)).convert("RGB")
        
        # XỬ LÝ NHẬN DIỆN THỰC TẾ
        predictions = pipe(image)
        # Lấy kết quả có độ tin cậy cao nhất (top 1)
        top_result = predictions[0]
        result = top_result['label']
        confidence = round(top_result['score'], 4)
        
        # 3. LƯU VÀO FIRESTORE 
        doc_ref = db.collection("detections").document()
        doc_ref.set({
            "user_id": user_id,
            "filename": file.filename,
            "result": result,
            "confidence": confidence,
            "note": note if note else "Không có ghi chú",
            "timestamp": firestore.SERVER_TIMESTAMP
        })
        
        return {
            "status": "success", 
            "result": result, 
            "confidence": confidence,
            "note": note
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint để xem lại lịch sử nhận diện 
@app.get("/history")
async def get_history(user_id: str):
    docs = db.collection("detections").where("user_id", "==", user_id).stream()
    history = [d.to_dict() for d in docs]
    return {"history": history}

@app.get("/stats")
async def get_stats(user_id: str):
    try:
        # Lấy tất cả bản ghi của user đó 
        docs = db.collection("detections").where("user_id", "==", user_id).stream()
        
        total_count = 0
        results_summary = {}
        
        for doc in docs:
            data = doc.to_dict()
            total_count += 1
            res = data.get("result", "Unknown")
            # Thống kê số lượng theo từng loại (ví dụ: bao nhiêu ảnh Dog, bao nhiêu ảnh Cat)
            results_summary[res] = results_summary.get(res, 0) + 1
            
        return {
            "user_id": user_id,
            "total_detections": total_count,
            "summary": results_summary
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))