import streamlit as st
import pandas as pd

# 1. 화면 설정 (광폭 레이아웃 사용)
st.set_page_config(page_title="일일 재고 현황표", layout="wide")

# 2. 이미지(5a975b) 기반 가로 지그재그 디자인 설정
st.markdown("""
<style>
    .title { text-align: center; font-size: 3.5em; font-weight: bold; text-decoration: underline; margin-bottom: 40px; }
    .board-container { display: flex; flex-direction: column; align-items: center; width: 100%; background-color: white; }
    
    /* 가로 배치를 강제하는 설정 */
    .stock-row { display: flex; flex-direction: row; justify-content: center; width: 100%; margin-bottom: -45px; }
    .row-offset { margin-left: 140px; } /* 지그재그 효과를 위해 홀수 줄을 오른쪽으로 밀기 */
    
    .stock-card {
        border: 1.5px solid #333; border-radius: 50%; width: 130px; height: 130px;
        display: flex; flex-direction: column; justify-content: center; align-items: center;
        background-color: white; margin: 10px; z-index: 2;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    }
    .item-name { font-weight: bold; color: #0000FF; font-size: 0.95em; }
    .item-qty { font-size: 1.3em; font-weight: bold; color: #000; margin: 3px 0; }
    .item-loc { color: #8DB48E; font-size: 0.85em; font-weight: bold; }
    
    /* 수량 0일 때 배경색과 글자색 스타일 */
    .out-of-stock { background-color: #FDF2F4; }
    .out-of-stock .item-qty { color: #FF0000; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">일 일 재 고 현 황 표</div>', unsafe_allow_html=True)

# 3. 데이터 관리 및 초기화 (37번 줄 에러 해결 구간)
if 'inventory_data' not in st.session_state:
    st.session_state['inventory_data'] = pd.DataFrame(columns=["품목명", "수량", "위치코드"])

# 4. 데이터 입력 섹션
st.subheader("📝 재고 데이터 입력")
edited_df = st.data_editor(
    st.session_state['inventory_data'],
    num_rows="dynamic",
    use_container_width=True,
    hide_index=True
