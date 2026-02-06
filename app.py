import streamlit as st
import pandas as pd

# 1. 페이지 설정 (가로로 넓게 사용)
st.set_page_config(page_title="일일 재고 현황표", layout="wide")

# 2. 디자인 스타일 (지그재그 가로 배치 및 원형 스타일)
st.markdown("""
<style>
    .title { text-align: center; font-size: 3.5em; font-weight: bold; text-decoration: underline; margin-bottom: 40px; }
    .board-container { display: flex; flex-direction: column; align-items: center; width: 100%; padding: 20px; background-color: white; }
    
    /* 가로 배치를 강제하는 레이아웃 */
    .stock-row { display: flex; flex-direction: row; justify-content: center; width: 100%; margin-bottom: -45px; }
    .row-offset { margin-left: 140px; } /* 지그재그 효과를 위한 밀기 */
    
    .stock-card {
        border: 1.5px solid #333; border-radius: 50%; width: 130px; height: 130px;
        display: flex; flex-direction: column; justify-content: center; align-items: center;
        background-color: white; margin: 10px; z-index: 2;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    }
    .item-name { font-weight: bold; color: #0000FF; font-size: 0.9em; text-align: center; }
    .item-qty { font-size: 1.2em; font-weight: bold; color: #000; margin: 2px 0; }
    .item-loc { color: #8DB48E; font-size: 0.8em; font-weight: bold; }
    
    /* 수량 0일 때 빨간색 강조 */
    .out-of-stock { background-color: #FDF2F4; }
    .out-of-stock .item-qty { color: #FF0000; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">일 일 재 고 현 황 표</div>', unsafe_allow_html=True)

# 3. 데이터 초기화 (35개 항목 고정 생성)
if 'inventory_data' not in st.session_state:
    st.session_state['inventory_data'] = pd.DataFrame({
        "
