import streamlit as st
import pandas as pd

# 1. 페이지 설정
st.set_page_config(page_title="재고 현황판", layout="wide")

# 2. 핵심 디자인 (이 코드가 그림을 만듭니다)
st.markdown("""
<style>
    .title { text-align: center; font-size: 40px; font-weight: bold; text-decoration: underline; margin-bottom: 20px; }
    .board { display: flex; flex-direction: column; align-items: center; width: 100%; background-color: #ffffff; }
    .row-cont { display: flex; flex-direction: row; justify-content: center; width: 100%; margin-bottom: -40px; }
    .zigzag { margin-left: 140px; } 
    .circle {
        border: 2px solid #333; border-radius: 50%; width: 120px; height: 120px;
        display: flex; flex-direction: column; justify-content: center; align-items: center;
        background-color: white; margin: 5px; flex-shrink: 0; box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    }
    .p-n { font-weight: bold; color: blue; font-size: 13px; text-align: center; }
    .p-q { font-size: 18px; font-weight: bold; color: black; }
    .p-l { color: green; font-size: 12px; font-weight: bold; }
    .zero { background-color: #fff1f0; }
    .zero .p-q { color: red; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">일 일 재 고 현 황 표</div>', unsafe_allow_html=True)

# 3. 데이터 준비 (35개 행)
if 'inven' not in st.session_state:
    st.session_state['inven'] = pd.DataFrame({
        "품목명": [""] * 35, "수량": [0] * 35, "위치코드": [""] * 35
    })

# 4. 입력 표 (상단)
