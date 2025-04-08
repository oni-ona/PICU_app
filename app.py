import streamlit as st
from PIL import Image
import time

# 페이지 설정
st.set_page_config(page_title="보호자 전용 로그인", layout="centered")

# 로고 이미지 (logo.png 파일이 같은 폴더에 있어야 함!)
logo = Image.open("logo.png")

# 세션 초기화
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "patient_id" not in st.session_state:
    st.session_state.patient_id = ""

# --------------------------
# 로그인 화면
# --------------------------
if not st.session_state.logged_in:

    # ⬆️ 로고 + 제목 + 안내문 (상단 고정)
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.image("logo.png", width=200)


    st.markdown("<h2 style='text-align: center;'> 💌 PICU 다이어리 💌 </h2>", unsafe_allow_html=True)
    st.markdown(
        "<p style='text-align: center; color: red; font-size: 0.9rem;'>"
        "*사전에 인증된 보호자만 접근할 수 있습니다.<br>"
        "접근권한이 없는 분들은 면회시간에 담당 의료진에게 문의해 주세요."
        "</p>",
        unsafe_allow_html=True
    )

    st.markdown("---")

    # ⬇️ 로그인 박스 (중앙 컴팩트)
    st.markdown("<div style='max-width: 400px; margin: auto;'>", unsafe_allow_html=True)

    with st.form("login_form"):
        patient_id = st.text_input("🆔 환자번호 ", max_chars=8)
        password = st.text_input("🔒 인증번호 ", type="password", max_chars=6)
        submitted = st.form_submit_button("로그인")

        if submitted:
            if patient_id == "12345678" and password == "220624":
                st.success("✅ 접속 중입니다. 잠시만 기다려주세요.")
                st.session_state.logged_in = True
                st.session_state.patient_id = patient_id
                time.sleep(1)
                st.rerun()
            else:
                st.error("❗️ 환자번호 또는 인증번호가 일치하지 않습니다.")

    st.markdown("</div>", unsafe_allow_html=True)

# --------------------------
# 로그인 성공 시 화면 (임시)
# --------------------------
else:
    col1, col2 = st.columns([10, 3])
    with col2:
        if st.button("처음으로 돌아가기"):
            st.session_state.logged_in = False
            st.session_state.patient_id = ""
            st.rerun()

    st.title("👶 로그인 성공!")
    st.markdown(f"환자번호: {st.session_state.patient_id}")
    st.markdown("> 이 아래는 목업 대시보드가 들어올 자리입니다.")
