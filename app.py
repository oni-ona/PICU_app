import streamlit as st
from PIL import Image
import time
from patient_data import mock_patient_data


# 페이지 설정
st.set_page_config(page_title="보호자 전용 로그인", layout="centered")

# 세션 초기화
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "patient_id" not in st.session_state:
    st.session_state.patient_id = ""

# --------------------------
# 로그인 화면
# --------------------------
if not st.session_state.logged_in:

    st.markdown("<h2 style='text-align: center;'> 💌 PICU 다이어리 💌 </h2>", unsafe_allow_html=True)
    st.markdown(
        "<p style='text-align: center; color: red; font-size: 0.9rem;'>"
        "사전에 인증된 보호자만 접근할 수 있습니다.<br>"
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

    st.markdown(
        "<div style='text-align: center; color: gray; font-size: 0.8rem; margin-top: 40px;'>"
        "본 사이트는 '소아중환자실 보호자를 위한 생성형 인공지능 기반의 임상 정보 자동 요약 시스템 개발 및 타당성 평가'<br>"
        "연구 과정의 일환으로 개발된 가상의 웹페이지이며, 모든 환자 정보는 가상의 정보임을 참고 부탁드립니다."
        "</div>",
        unsafe_allow_html=True
    )

else:
    # 1. 상단 우측: 뒤로가기
    col1, col2 = st.columns([10, 3])
    with col2:
        if st.button("처음으로 돌아가기"):
            st.session_state.logged_in = False
            st.session_state.patient_id = ""
            st.rerun()

    # 2. 환자 데이터 가져오기
    patient = mock_patient_data[st.session_state.patient_id]

    # 3. 입실일 기준 날짜 계산
    from datetime import datetime
    admission_date = datetime.strptime(patient["admission_date"], "%Y.%m.%d")
    days_in_picu = (datetime.today() - admission_date).days

    # 4. 상단 헤더
    # 상단 헤더 꾸미기
    st.markdown(
        f"<h2 style='text-align: center;'> {patient['name']} 보호자님, 안녕하세요!</h2>",
        unsafe_allow_html=True
    )
    st.markdown(
        f"<h3 style='text-align: center; color: #333;'> 오늘은 PICU 입실 {days_in_picu}일 째입니다.</h3>",
        unsafe_allow_html=True
    )
    st.markdown("---")


    # 5. 상단 2단 (몸무게 & 요약)
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📈 몸무게")

        import plotly.graph_objects as go
        from datetime import datetime

        weight_dict = patient["weight"]
        dates = [
            datetime.strptime(d, "%Y.%m.%d").strftime("%m.%d") 
            for d in weight_dict.keys()
        ]
        weights = list(weight_dict.values())

        min_y = int(min(weights)) - 1
        max_y = int(max(weights)) + 1
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=dates,
            y=weights,
            mode='lines+markers',
            name='체중',
            line=dict(width=3),
            marker=dict(size=8),
            hovertemplate='%{y}kg<extra></extra>'
        ))

        # 축 커스터마이징
        fig.update_layout(
            xaxis_title="날짜",
            yaxis_title="체중 (kg)",
            yaxis=dict(
                tick0=round(min_y, 1),
                dtick=0.5,
                range=[min_y, max_y]
            ),
            xaxis=dict(
                tickangle=0
            ),
            height=400,
            margin=dict(l=30, r=30, t=60, b=30),
            template="simple_white"
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
            config={"displayModeBar": False})


    with col2:
        st.subheader("📝 오늘의 요약")
        st.markdown(patient["summary"])

        st.markdown(
            f"<p style='text-align: right; font-size: 0.8rem; color: gray;'>"
            f"마지막 업데이트: {patient['last_updated']}</p>",
            unsafe_allow_html=True
        )


    # 6. 하단 (검사 & 질문)
    st.markdown("---")
    col3, col4 = st.columns(2)

    with col3:
        st.subheader("🧪 검사 결과")
        st.markdown(
            "<p style='font-size: 0.75rem; color: red;'>"
            "해당 내용은 일반적인 설명으로, 환자마다 다르게 해석될 수 있습니다.<br>"
            "자세한 사항은 담당 의료진과 상의하세요."
            "</p>",
            unsafe_allow_html=True
        )
        with st.expander("🩸 혈액검사"):
            st.markdown("""
            <h6>
            <span title="hs-CRP는 고감도 C-반응단백 검사로, 여러가지 염증반응이나 조직손상을 확인하기 위한 검사입니다.">
            • hs-CRP
            </span>
            </h6>
            """, unsafe_allow_html=True)

            st.markdown(
                "<p style='font-size: 0.75rem; color: gray; margin-bottom: 6px;'>"
                "참고치: 0.0 ~ 0.5 (mg/dL)"
                "</p>",
                unsafe_allow_html=True
            )

            crp_results = {
                "2025.09.07": 0.28,
                "2025.09.11": 5.33
            }

            sorted_dates = sorted(crp_results.keys())
            previous_date = sorted_dates[-2]
            latest_date = sorted_dates[-1]
            previous_value = crp_results[previous_date]
            latest_value = crp_results[latest_date]

            color = "red" if latest_value > previous_value else "green"

            st.markdown(f"""
            <div style='
                border: 1px solid #ccc;
                border-radius: 10px;
                padding: 10px;
                background-color: #f9f9f9;
                font-size: 0.95rem;
            '>
                <b>{previous_date}</b>: {previous_value} mg/dL  
                <br><b>{latest_date}</b>:
                <span style='color:{color};'>{latest_value} mg/dL</span>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("""
            <h6 style='margin-top: 12px; margin-bottom: 2px;'>
            <span title="PCT(프로칼시토닌)는 세균 감염에 반응하는 물질로, 세균성 패혈증을 확인하기 위한 검사입니다.">
            • PCT
            </span>
            </h6>
            """, unsafe_allow_html=True)

            st.markdown(
                "<p style='font-size: 0.75rem; color: gray; margin-bottom: 6px;'>"
                "참고치: 0.0 ~ 0.5 (ng/mL)"
                "</p>",
                unsafe_allow_html=True
            )

            st.markdown(f"""
            <div style='
                border: 1px solid #ccc;
                border-radius: 10px;
                padding: 10px;
                background-color: #f9f9f9;
                font-size: 0.95rem;
            '>
                <b style='font-size: 0.85rem;'>직전 결과</b>: <span style='font-size: 0.85rem;'>없음</span>
                <br><b>2025.09.11</b>: 
                <span style='font-size: 0.85rem;'>결과 보고 중</span>
            </div>
            """, unsafe_allow_html=True)

        with st.expander("🦠 배양검사"):
            st.markdown("• RV PCR (2025.08.22): Rhinovirus **Positive**")
            st.markdown("• RV PCR (2025.09.11): 검사 진행 중")
            st.markdown("• Urine Cx (2025.09.22): 검사 진행 중")
        
        with st.expander("🩻 영상검사"):
            st.markdown("• Chest AP(2025.08.22): No interval change")
            st.markdown("• Chest AP(2025.09.11): No interval change")
    
    st.markdown("---")

    with col4:
        st.subheader("💬 다른 궁금한 사항이 있나요?")
        
        if "question_log" not in st.session_state:
            st.session_state.question_log = []

        input_col, button_col = st.columns([6, 2])

        with input_col:
            question = st.text_input(
                "바로 확인은 어려운 점 양해 부탁드립니다.🙏🏻",
                placeholder="궁금한 내용을 입력해주세요."
            )

        with button_col:
            st.write("")
            st.write("")
            if st.button("확인", use_container_width=False):
                timestamp = datetime.now().strftime("2025.09.12 %p %I:%M")
                st.session_state.question_log.append(f"{timestamp} - {question}")

    
        if st.session_state.question_log:
            st.markdown("**🗒️ 보호자님의 남긴 질문:**")
            for q in reversed(st.session_state.question_log):  # 최근순 정렬
                st.markdown(f"- {q}")
        
    st.markdown(
        "<div style='text-align: center; color: gray; font-size: 0.8rem; margin-top: 40px;'>"
        "본 사이트는 '소아중환자실 보호자를 위한 생성형 인공지능 기반의 임상 정보 자동 요약 시스템 개발 및 타당성 평가'<br>"
        "연구 과정의 일환으로 개발된 가상의 웹페이지이며, 모든 환자 정보는 가상의 정보임을 참고 부탁드립니다."
        "</div>",
        unsafe_allow_html=True
    )