import streamlit as st
import pandas as pd

# 1. 화면 설정
st.set_page_config(page_title="일일 재고 현황표", layout="wide")

# 2. 디자인 스타일 (지그재그 배치 및 색상 설정)
st.markdown("""
<style>
    .title { text-align: center; font-size: 3.5em; font-weight: bold; text-decoration: underline; margin-bottom: 30px; }
    .board-container { display: flex; flex-direction: column; align-items: center; background-color: white; padding: 20px; }
    .stock-row { display: flex; justify-content: center; width: 100%; margin-bottom: -35px; }
    .row-offset { padding-left: 140px; }
    .stock-card {
        border: 1.5px solid #333; border-radius: 50%; width: 130px; height: 130px;
        display: flex; flex-direction: column; justify-content: center; align-items: center;
        background-color: white; margin: 5px; z-index: 2;
    }
    .item-name { font-weight: bold; color: #0000FF; font-size: 1em; }
    .item-qty { font-size: 1.3em; font-weight: bold; color: #000; margin: 2px 0; }
    .item-loc { color: #8DB48E; font-size: 0.9em; font-weight: bold; }
    .out-of-stock { background-color: #FDF2F4; }
    .out-of-stock .item-qty { color: #FF0000; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">일 일 재 고 현 황 표</div>', unsafe_allow_html=True)

# 3. 데이터 초기화
if 'inventory_data' not in st.session_state:
    st.session_state.inventory_data = pd.DataFrame(columns=["품목명", "수량", "위치코드"])

st.subheader("📝 재고 데이터 입력")
# 데이터 편집기
edited_df = st.data_editor(
    st.session_state.inventory_data, 
    num_rows="dynamic", 
    use_container_width=True, 
    hide_index=True
)

# 수정 내용 적용 버튼
if st.button("수정 내용 적용하기"):
    if edited_df is not None
