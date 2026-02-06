import streamlit as st
import pandas as pd

# 1. 화면 설정
st.set_page_config(page_title="일일 재고 현황표", layout="wide")

# 2. 스타일 설정 (지그재그 및 색상)
st.markdown("""
<style>
    .title { text-align: center; font-size: 3.5em; font-weight: bold; text-decoration: underline; margin-bottom: 30px; }
    .board-container { display: flex; flex-direction: column; align-items: center; background-color: white; padding: 20px; }
    .stock-row { display: flex; justify-content: center; width: 100%; margin-bottom: -35px; }
    .row-offset { padding-left: 140px; } /* 지그재그 효과를 위한 옆으로 밀기 */
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

st.subheader("📝 재고 편집")
edited_df = st.data_editor(st.session_state.inventory_data, num_rows="dynamic", use_container_width=True, hide_index=True)

if st.button("수정 내용 적용하기"):
    if edited_df is not None:
        df_new = edited_df.dropna(subset=["품목명"]).copy()
        st.session_state.inventory_data = df_new[df_new["품목명"].astype(str).str.strip() != ""]
        st.rerun()

st.divider()

# 4. 지그재그 현황판 출력
df = st.session_state.inventory_data
if not df.empty:
    st.markdown('<div class="board
