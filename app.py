import streamlit as st
import pandas as pd

# 1. 화면 설정 (광폭 레이아웃)
st.set_page_config(page_title="일일 재고 현황표", layout="wide")

# 2. 디자인 스타일 (지그재그 가로 배치 및 원형 스타일)
st.markdown("""
<style>
    .title { text-align: center; font-size: 3.5em; font-weight: bold; text-decoration: underline; margin-bottom: 40px; }
    .board-container { display: flex; flex-direction: column; align-items: center; width: 100%; background-color: white; padding: 20px; }
    
    /* 가로 배치를 위한 레이아웃 */
    .stock-row { display: flex; flex-direction: row; justify-content: center; width: 100%; margin-bottom: -45px; }
    .row-offset { margin-left: 140px; } /* 지그재그 효과 */
    
    .stock-card {
        border: 1.5px solid #333; border-radius: 50%; width: 130px; height: 130px;
        display: flex; flex-direction: column; justify-content: center; align-items: center;
        background-color: white; margin: 10px; z-index: 2;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    }
    .item-name { font-weight: bold; color: #0000FF; font-size: 0.9em; text-align: center; padding: 0 5px; }
    .item-qty { font-size: 1.2em; font-weight: bold; color: #000; margin: 2px 0; }
    .item-loc { color: #8DB48E; font-size: 0.8em; font-weight: bold; }
    
    /* 수량 0 스타일 */
    .out-of-stock { background-color: #FDF2F4; }
    .out-of-stock .item-qty { color: #FF0000; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">일 일 재 고 현 황 표</div>', unsafe_allow_html=True)

# 3. 데이터 초기화 (35개 행 고정 - 에러가 났던 구간 완벽 수정)
if 'inventory_data' not in st.session_state:
    initial_data = pd.DataFrame({
        "품목명": [""] * 35, 
        "수량": [None] * 35, 
        "위치코드": [""] * 35
    })
    st.session_state['inventory_data'] = initial_data

# 4. 데이터 입력 표 (상단에 35개 행 유지)
st.subheader("📝 재고 데이터 입력 (35개 항목)")
edited_df = st.data_editor(
    st.session_state['inventory_data'],
    num_rows="fixed",
    use_container_width=True,
    hide_index=False,
    key="inventory_editor"
)

# [수정 내용 적용하기] 버튼
if st.button("수정 내용 적용하기"):
    if edited
