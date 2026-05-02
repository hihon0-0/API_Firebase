import streamlit as st
import requests
import pandas as pd

# Địa chỉ Backend FastAPI của bạn
BACKEND_URL = "http://127.0.0.1:8000"

# Cấu hình giao diện trang web 
st.set_page_config(page_title="AI Detector", layout="wide")

# Khởi tạo trạng thái đăng nhập trong session_state
if 'uid' not in st.session_state:
    st.session_state['uid'] = None
if 'email' not in st.session_state:
    st.session_state['email'] = None

# THANH SIDEBAR: QUẢN LÝ TÀI KHOẢN 
with st.sidebar:
    st.header("🔐 Tài khoản")
    
    if not st.session_state['uid']:
        # Lựa chọn giữa Đăng nhập và Đăng ký
        auth_mode = st.radio("Lựa chọn:", ["Đăng nhập", "Đăng ký"])
        
        if auth_mode == "Đăng nhập":
            # Lựa chọn phương thức đăng nhập theo ý bạn
            method = st.selectbox("Phương thức đăng nhập:", ["Dùng Email/Mật khẩu", "Dùng UID (Demo nhanh)"])
            
            if method == "Dùng Email/Mật khẩu":
                email_in = st.text_input("Email:")
                pass_in = st.text_input("Mật khẩu:", type="password")
                if st.button("Xác nhận Đăng nhập"):
                    res = requests.post(f"{BACKEND_URL}/auth/login", json={"email": email_in, "password": pass_in})
                    if res.status_code == 200:
                        data = res.json()
                        st.session_state.update({"uid": data['uid'], "email": data['email']})
                        st.success("Đăng nhập thành công!")
                        st.rerun()
                    else:
                        st.error("Sai Email hoặc Mật khẩu!")
            
            else: # Đăng nhập bằng UID
                uid_in = st.text_input("Dán UID vào đây:", type="password")
                if st.button("Đăng nhập bằng UID"):
                    res = requests.post(f"{BACKEND_URL}/auth/login", json={"uid": uid_in})
                    if res.status_code == 200:
                        data = res.json()
                        st.session_state.update({"uid": data['uid'], "email": data['email']})
                        st.success("Đăng nhập thành công!")
                        st.rerun()
                    else:
                        st.error("UID không hợp lệ!")
        
        else: # Chế độ Đăng ký
            reg_email = st.text_input("Email mới:")
            reg_pass = st.text_input("Mật khẩu mới:", type="password")
            if st.button("Tạo tài khoản"):
                res = requests.post(f"{BACKEND_URL}/auth/register", json={"email": reg_email, "password": reg_pass})
                if res.status_code == 200:
                    st.success("Đăng ký thành công! Hãy chuyển sang Đăng nhập.")
                else:
                    st.error(f"Lỗi: {res.json().get('detail')}")
    else:
        # Hiển thị khi đã đăng nhập thành công 
        st.success("Đã đăng nhập!")
        st.write(f"📧 **Email:** {st.session_state['email']}")
        st.write(f"🆔 **UID:** `{st.session_state['uid']}`")
        if st.button("Đăng xuất"):
            st.session_state['uid'] = None
            st.session_state['email'] = None
            st.rerun()

# NỘI DUNG CHÍNH CỦA ỨNG DỤNG
st.title("🖼️ Hệ thống Nhận diện Hình ảnh thông minh")

if st.session_state['uid']:
    # Chia các chức năng thành các Tab 
    tab1, tab2, tab3 = st.tabs(["🚀 Phân tích ảnh", "📊 Thống kê", "📜 Lịch sử"])

    # TAB 1: FEATURE CHÍNH (NHẬN DIỆN & GHI CHÚ) 
    with tab1:
        st.subheader("Tải ảnh và Nhận diện")
        uploaded_file = st.file_uploader("Chọn ảnh (jpg, png)...", type=["jpg", "png", "jpeg"])
    
        user_note = st.text_area("Thêm ghi chú cho ảnh này:", placeholder="Ví dụ: ảnh tui lấy trên mạng, nó là meme...")

        if st.button("Phân tích ảnh"):
            if uploaded_file:
                with st.spinner("AI đang phân tích..."):
                    # Gửi ảnh và ghi chú lên Backend 
                    files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                    payload = {"user_id": st.session_state['uid'], "note": user_note}
                    
                    res = requests.post(f"{BACKEND_URL}/detect", files=files, data=payload)
                    
                    if res.status_code == 200:
                        result = res.json()
                        st.success(f"**Kết quả nhận diện:** {result['result']}")
                        st.info(f"**Ghi chú:** {result['note']}")
                        st.image(uploaded_file, width=400)
                    else:
                        st.error("Lỗi khi xử lý ảnh trên Backend.")
            else:
                st.warning("Vui lòng chọn ảnh trước!")

    # TAB 2: THỐNG KÊ (READ DATABASE) 
    with tab2:
        st.subheader("Thống kê dữ liệu của bạn")
        res_stats = requests.get(f"{BACKEND_URL}/stats", params={"user_id": st.session_state['uid']})
        if res_stats.status_code == 200:
            stats_data = res_stats.json()
            st.metric("Tổng số lần đã nhận diện", stats_data['total_detections'])
            
            if stats_data['summary']:
                df = pd.DataFrame(list(stats_data['summary'].items()), columns=['Đối tượng', 'Số lượng'])
                st.bar_chart(df.set_index('Đối tượng'))

    # TAB 3: LỊCH SỬ (READ DATABASE)
    with tab3:
        st.subheader("Lịch sử nhận diện chi tiết")
        res_hist = requests.get(f"{BACKEND_URL}/history", params={"user_id": st.session_state['uid']})
        if res_hist.status_code == 200:
            history = res_hist.json().get('history', [])
            if history:
                for item in reversed(history):
                    with st.expander(f"🕒 {item.get('timestamp')} - {item.get('result')}"):
                        st.write(f"📝 **Ghi chú:** {item.get('note')}")
                        st.write(f"🎯 **Độ tin cậy:** {item.get('confidence')}")
            else:
                st.write("Bạn chưa có dữ liệu lịch sử nào.")
else:
    st.info("👋 Chào bạn! Vui lòng Đăng nhập hoặc Đăng ký từ thanh bên trái để bắt đầu sử dụng.")