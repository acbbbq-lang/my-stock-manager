import streamlit as st
import pandas as pd

# 1. 페이지 설정 (넓은 화면 사용)
st.set_page_config(page_title="일일 재고 현황표", layout="wide")

# 2. CSS 디자인 (가로 7개씩 5줄 배치 강제)
st.markdown("""
<style>
    .title { text-align: center; font-size: 3em; font-weight: bold; text-decoration: underline; margin-bottom: 30px; }
    .main-board { display: flex; flex-direction: column; align-items: center; width: 100%; background-color: white; }
    
    /* 가로 배치를 위한 컨테이너 */
    .row-cont { 
        display: flex; 
        flex-direction: row; 
        justify-content: center; 
        width: 100%; 
        margin-bottom: -45px; 
    }
    
    /* 지그재그 오프셋 효과 */
    .zigzag { margin-left: 140px; } 

    .circle {
        border: 2px solid #333; border-radius: 50%; 
        width: 125px; height: 125px;
        display: flex; flex-direction: column; justify-content: center; align-items: center;
        background-color: white; margin: 8px; flex-shrink: 0;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    }
    .p-n { font-weight: bold; color: blue; font-size: 0.85em; text-align: center; }
    .p-q { font-size: 1.1em; font-weight: bold; color: black; margin: 2px 0; }
    .p-l { color: green; font-size: 0.75em; font-weight: bold; }
    .zero { background-color: #fff1f0; }
    .zero .p-q { color: red; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">일 일 재 고 현 황 표</div>', unsafe_allow_html=True)

# 3. 데이터 초기화 (35개 행 고정)
if 'inven' not in st.session_state:
    st.session_state['inven'] =
