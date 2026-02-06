import streamlit as st
import pandas as pd
from io import StringIO

# 1. 페이지 설정
st.set_page_config(page_title="일일 재고 현황표", layout="wide")

# 2. CSS: 네모 확대 및 위아래 공백 제거 (자석 밀착)
st.markdown("""
<style>
    .title { text-align: center; font-size: 3em; font-weight: bold; text-decoration: underline; margin-bottom: 20px; }
    
    .main-container {
        display: flex; flex-direction: column; align-items: center; width: 100%;
    }

    .row-cont { 
        display: flex; 
        justify-content: center; 
        width: 100%; 
        /* 네모가 커진 만큼 겹침 강도를 -85px로 설정하여 위아래 공백 제거 */
        margin-bottom: -85px; 
        position: relative;
    }

    .row-cont:last-child { margin-bottom: 100px; }

    .layer-top { z-index: 100; }
    .layer-bottom { z-index: 50; }

    .card {
        display: flex; flex-direction: column; justify-content: center; align-items: center;
        background-color: white; border: 2.5px solid #000;
        margin: 0 -8px; flex-shrink: 0;
        box-shadow: 2px 2px 6px rgba(0,0,0,0.1);
    }

    /* 동그라미: 기존 크기 유지 */
    .shape-circle { width: 130px; height: 130px; border-radius: 50%; }

    /* 네모: 크기 대폭 확대 (가로 190px, 세로 170px) */
    .shape-square { 
        width: 190px; height: 170px; 
        border-radius: 10px; 
        background-color: #fcfcfc;
    }

    /* 텍스트 스타일: 네모가 커진 만큼 폰트도 키움 */
    .p-n { font-weight: bold; font-size: 16px; margin-bottom: 4px; }
    .p-q { font-size: 26px; font-weight: 900; color: #000; line-height: 1.0; }
    .p-l { color: #8eb44e; font-size: 14px; font-weight: bold; margin-top: 4px; }
    
    .t-blue { color: #0000FF; }
    .t-orange { color: #d35400; }
    .zero-bg { background-color: #fff1f0; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">일 일 재 고 현 황 표</div>', unsafe_allow_html=True)

# 3. 데이터 로직
if 'inven' not in st.session_state:
    st.session_state['inven'] = pd.DataFrame({
        "품목명": ["-"] * 35,
        "수량": [0] * 35,
        "위치코드": ["-"] * 35
    })

# --- 엑셀 복사 붙여넣기 칸 ---
with st.expander("📋 엑셀 데이터 통째로 붙여넣기"):
    st.info("엑셀에서 품목명, 수량, 위치코드 3개 열을 복사(Ctrl+C)해서 아래에 붙여넣으세요.")
    input_text = st.text_area("여기에 붙여넣기 (Ctrl+V)", height=150)
    
    if st.button("붙여넣은 데이터 즉시 반영"):
        if input_text:
            try:
                # 탭 구분자로 읽기 (엑셀 복사 표준)
                new_df = pd.read_csv(StringIO(input_text), sep='\t', names=["품목명", "수량", "위치코드"])
                # 35개 행으로 규격 맞춤
                if len(new_df) < 35:
                    extra = pd.DataFrame([["-", 0, "-"]] * (35 - len(new_df)), columns=["품목명", "수량", "위치코드"])
                    new_df = pd.concat([new_df, extra],
