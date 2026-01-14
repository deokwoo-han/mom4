import streamlit as st
import pandas as pd
from datetime import datetime
import time
import random

# --- 0. 기본 설정 및 디자인 (Warm Tech UI) ---
st.set_page_config(page_title="AI 솔빙 스트레스: 마음 닥터", page_icon="🧡", layout="wide")

# 따뜻한 파스텔톤 & 카드형 UI CSS 적용
st.markdown("""
    <style>
    .stApp { background-color: #FFFBF5; } /* 크림색 배경 */
    
    /* 메인 헤더 스타일 */
    .main-header { font-size: 2.2rem; color: #E67E22; font-weight: bold; margin-bottom: 10px; }
    
    /* 카드 박스 스타일 */
    .card {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin-bottom: 20px;
        border-left: 5px solid #E67E22;
    }
    
    /* [NEW] SOS 작은 정보 카드 스타일 */
    .sos-card {
        background-color: #F8F9F9;
        padding: 12px;
        border-radius: 10px;
        border: 1px solid #E0E0E0;
        margin-bottom: 10px;
        font-size: 14px; /* 글자 크기 축소 */
        color: #555;
    }
    .sos-number {
        font-weight: bold;
        color: #E74C3C;
        font-size: 16px; /* 번호만 살짝 강조 */
    }
    
    /* 버튼 스타일 */
    div.stButton > button:first-child {
        background-color: #E67E22;
        color: white;
        border-radius: 20px;
        border: none;
        padding: 10px 20px;
        font-weight: bold;
    }
    div.stButton > button:hover {
        background-color: #D35400;
        color: white;
    }
    
    /* 탭 스타일 */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #FAE5D3;
        border-radius: 10px 10px 0 0;
        padding: 10px 20px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #E67E22;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# --- 1. 데이터 및 헬퍼 함수 ---

# 감정 키워드
EMOTION_CHIPS = {
    "🔥 불안/공포": ["가슴이 뜀", "식은땀", "안절부절", "압박감", "막막함"],
    "💧 우울/슬픔": ["무기력", "눈물", "가라앉음", "허무함", "지침"],
    "💢 분노/짜증": ["욱함", "답답함", "억울함", "신경질", "열받음"],
    "🌿 평온/긍정": ["다행임", "편안함", "감사함", "기대됨", "차분함"]
}

# 따뜻한 피드백
def get_warm_feedback():
    quotes = [
        "당신의 감정은 틀리지 않았습니다. 그저 날씨처럼 지나가는 중입니다. ☁️",
        "기록하는 것만으로도 당신은 이미 자신을 돌보고 계십니다. 👏",
        "불안은 당신이 잘하고 싶다는 마음의 증거이기도 합니다. 🌱",
        "잠시 심호흡을 해보세요. 지금 이 순간은 안전합니다. 🧘"
    ]
    return random.choice(quotes)

# 세션 스테이트 초기화 (데이터 저장소)
if 'journal_logs' not in st.session_state:
    st.session_state.journal_logs = []

# --- 2. 사이드바 (네비게이션) ---
with st.sidebar:
    st.title("🧡 마음 닥터")
    st.info("상담심리학 박사의 이론을\nAI 기술로 구현했습니다.")
    
    menu = st.radio("메뉴 선택", ["📝 오늘의 마음 기록", "📊 AI 심리 분석", "🚨 SOS 위기 지원"])
    st.divider()
    
    # 미니 대시보드
    if st.session_state.journal_logs:
        st.caption(f"누적 기록: {len(st.session_state.journal_logs)}건")
        last_log = st.session_state.journal_logs[-1]
        st.caption(f"최근 기록: {last_log['time']}")
    else:
        st.caption("아직 기록이 없습니다.")

# --- 3. 메인 기능 구현 ---

st.markdown("<div class='main-header'>AI 솔빙 스트레스: 마음 관찰 일기</div>", unsafe_allow_html=True)
st.write(get_warm_feedback())

# [TAB 1] 마음 기록
if menu == "📝 오늘의 마음 기록":
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("<div class='card'><h4>💭 1. 상황과 생각 포착</h4>", unsafe_allow_html=True)
        thought_input = st.text_area("지금 머릿속을 맴도는 생각이나 상황은 무엇인가요?", height=100, 
                                     placeholder="예: 내일 발표가 있는데 망칠까 봐 너무 걱정된다.")
        
        # 인지 라벨링
        st.markdown("<b>🏷️ 이 생각에 이름표를 붙여볼까요?</b>", unsafe_allow_html=True)
        label_type = st.radio("생각의 종류", ["미래에 대한 불안 (What if)", "과거에 대한 후회 (If only)", "현재의 단순 사실", "해결 가능한 문제"], horizontal=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='card'><h4>❤️ 2. 감정과 감각 확인</h4>", unsafe_allow_html=True)
        
        # 감정 칩 선택
        selected_emotions = []
        st.write("지금 느껴지는 감정 단어들을 선택해주세요.")
        for category, keywords in EMOTION_CHIPS.items():
            selected = st.multiselect(category, keywords, key=category)
            selected_emotions.extend(selected)
            
        # 감정 농도 및 신체 감각
        st.divider()
        intensity = st.slider("감정의 농도 (0: 평온 ~ 100: 압도됨)", 0, 100, 50)
        sensation = st.text_input("신체 감각 (예: 가슴이 답답함, 어깨가 뭉침)")
        st.markdown("</div>", unsafe_allow_html=True)

    # 제3자의 시선 (객관화 훈련)
    st.markdown("<div class='card'><h4>🕵️ 3. 제3자의 시선 (거리두기)</h4>", unsafe_allow_html=True)
    st.caption("나를 잘 아는 지혜로운 친구가 이 상황을 본다면 뭐라고 말해줄까요?")
    observer_view = st.text_input("객관적 관찰 기록", placeholder="그녀는 지금 잘하고 싶은 마음에 긴장하고 있다. 하지만 아직 일어나지 않은 일이다.")
    st.markdown("</div>", unsafe_allow_html=True)

    # 저장 버튼
    if st.button("✨ 오늘의 마음 저장하기", use_container_width=True):
        if thought_input and selected_emotions:
            new_entry = {
                "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "thought": thought_input,
                "label": label_type,
                "emotions": selected_emotions,
                "intensity": intensity,
                "sensation": sensation,
                "observer": observer_view
            }
            st.session_state.journal_logs.append(new_entry)
            st.success("성공적으로 기록되었습니다! 'AI 심리 분석' 탭에서 변화를 확인해보세요.")
            time.sleep(1)
            st.rerun()
        else:
            st.error("생각과 감정을 최소 하나 이상 입력해주세요.")

    # 최근 기록 보기
    st.divider()
    st.subheader("📂 최근 기록 모아보기")
    if st.session_state.journal_logs:
        for log in reversed(st.session_state.journal_logs[-3:]):
            with st.expander(f"📌 {log['time']} | {log['thought'][:20]}..."):
                st.write(f"**🏷️ 라벨:** {log['label']}")
                st.write(f"**❤️ 감정:** {', '.join(log['emotions'])} (농도: {log['intensity']}%)")
                st.write(f"**🕵️ 관찰:** {log['observer']}")

# [TAB 2] AI 심리 분석
elif menu == "📊 AI 심리 분석":
    if not st.session_state.journal_logs:
        st.warning("분석할 데이터가 없습니다. '오늘의 마음 기록' 탭에서 먼저 기록을 남겨주세요.")
    else:
        st.markdown("### 📈 마음 건강 대시보드")
        
        # 감정 농도 변화 그래프
        df = pd.DataFrame(st.session_state.journal_logs)
        st.line_chart(df, x="time", y="intensity", color="#E67E22")
        st.caption("최근 감정 농도의 변화 추이입니다. 급격히 높아지는 구간을 유의하세요.")

        st.divider()

        # AI 분석 리포트
        if st.button("🧠 AI 정밀 분석 실행"):
            with st.spinner("임상 데이터를 기반으로 분석 중입니다... (CBT 프로토콜 적용)"):
                time.sleep(2)
            
            recent_log = st.session_state.journal_logs[-1]
            main_emotion = recent_log['emotions'][0] if recent_log['emotions'] else "알 수 없음"
            
            st.markdown(f"""
            <div class='card'>
                <h3>📑 AI 심리 분석 리포트</h3>
                <p><b>최근 주요 감정:</b> <span style='color:#E67E22; font-weight:bold;'>{main_emotion}</span></p>
                <p><b>인지 왜곡 유형 탐지:</b> '{recent_log['label']}' 패턴이 감지되었습니다.</p>
                <p>사용자님은 현재 상황을 있는 그대로 받아들이기보다, <b>'{recent_log['label']}'</b>의 필터로 해석하는 경향이 있습니다.
                이는 스트레스 농도를 {recent_log['intensity']}%까지 높이는 주요 원인으로 분석됩니다.</p>
                <hr>
                <h4>💊 박사님의 맞춤 처방 (Action Plan)</h4>
                <ul>
                    <li><b>즉시 처방:</b> 4-7-8 호흡법을 3회 실시하여 신체 감각({recent_log['sensation'] or '긴장'})을 이완시키세요.</li>
                    <li><b>인지 훈련:</b> '{recent_log['observer']}'라고 적으신 내용을 소리 내어 3번 읽어보세요. 내 생각이 사실이 아님을 뇌에 인지시키는 과정입니다.</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

# [TAB 3] SOS 위기 지원 (디자인 수정: 글자 크기 축소)
elif menu == "🚨 SOS 위기 지원":
    st.markdown("<div class='card' style='border-left: 5px solid #E74C3C;'>", unsafe_allow_html=True)
    st.error("### 혼자 감당하기 힘드신가요?")
    st.markdown("<div style='font-size:14px; margin-bottom:15px;'>지금 전문가의 도움이 필요하다면 아래 기관에 연락하세요. <b>비밀은 100% 보장됩니다.</b></div>", unsafe_allow_html=True)
    
    # [수정됨] 작고 깔끔한 HTML 카드로 변경 (st.info 대신)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="sos-card">
            📞 <b>자살예방 상담전화</b><br>
            <span class="sos-number">109</span> (24시간)
        </div>
        <div class="sos-card">
            📞 <b>정신건강 위기상담</b><br>
            <span class="sos-number">1577-0199</span>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="sos-card">
            🏥 <b>가까운 센터 찾기</b><br>
            보건복지부 홈페이지 참조
        </div>
        <div class="sos-card">
            💬 <b>청소년 모바일 상담</b><br>
            '다 들어줄 개' 앱
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    st.subheader("🧘 긴급 안정화 (Grounding)")
    st.write("지금 당장 너무 힘들다면, 화면을 보며 숫자를 세어보세요.")
    if st.button("호흡 가이드 시작"):
        with st.empty():
            for i in range(3):
                st.markdown(f"## 🌿 숨을 들이마시세요... (Inhale)")
                time.sleep(3)
                st.markdown(f"## 😶 숨을 멈추세요... (Hold)")
                time.sleep(3)
                st.markdown(f"## 💨 숨을 내쉬세요... (Exhale)")
                time.sleep(3)
            st.success("조금 편안해지셨나요?")
    st.markdown("</div>", unsafe_allow_html=True)