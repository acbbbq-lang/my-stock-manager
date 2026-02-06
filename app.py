import streamlit as st
import pandas as pd

# 1. 페이지 설정
st.set_page_config(page_title="일일 재고 현황표", layout="wide")

# 2. CSS 설정 (가로 배치 및 지그재그 핵심 디자인)
st.markdown("""
<style>
    .title { text-align: center; font-size: 3em; font-weight: bold; text-decoration: underline; margin-bottom: 30px; }
    .main-board { display: flex; flex-direction: column; align-items: center; width: 100%; }
    
    /* 한 줄(7개)을 감싸는 컨테이너: 가로 정렬 */
    .row-container { 
        display: flex; 
        justify-content: center; 
        width: 100%; 
        margin-bottom: -45px; /* 줄 간격 겹침 */
    }
    
    /* 지그재그 오프셋 */
    .zigzag { margin-left: 140px; } 

    .stock-card {
        border: 2px solid #333; border-radius: 50%; 
        width: 130px; height: 130px;
        display: flex; flex-direction: column; justify-content: center; align-items: center;
        background-color: white; margin: 10px; flex-shrink: 0;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    }
    .p-name { font-weight: bold; color: blue; font-size: 0.9em; text-align: center; }
    .p-qty { font-size: 1.2em; font-weight: bold; color: black; margin: 2px 0; }
    .p-loc { color: green; font-size: 0.8em; font-weight: bold; }
    .out { background-color: #fff1f0; }
    .out .p-qty { color: red; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">일 일 재 고 현 황 표</div>', unsafe_allow_html=True)

# 3. 데이터 초기화 (35개 항목)
if 'inven' not in st.session_state:
    st.session_state['in
