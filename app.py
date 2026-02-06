import streamlit as st
import pandas as pd

# 1. 화면 전체 너비 사용
st.set_page_config(page_title="일일 재고 현황표", layout="wide")

# 2. 이미지와 동일한 지그재그 가로 정렬 디자인 (CSS)
st.markdown("""
<style>
    .title { text-align: center; font-size: 3.5em; font-weight: bold; text-decoration: underline; margin-bottom: 40px; }
    
    /* 전체 판: 모든 줄을 중앙으로 모음 */
    .board-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        width: 100%;
    }

    /* 한 줄(Row): 가로로 나열(row) */
    .stock-row {
        display: flex;
        flex-direction: row; /* 가로 배치 강제 */
        justify-content: center;
        width: 100%;
        margin-bottom: -45px; /* 줄 사이를 겹치게 하여 지그재그 효과 */
    }

    /* 지그재그 오프셋: 짝수 줄을 오른쪽으로 밀기 */
    .row-offset {
        margin-left: 140px;
    }

    .stock-card {
        border: 1.5px solid #333;
        border-radius: 50%;
        width: 130px;
        height: 130px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        background-color: white;
        margin: 10px;
        z-index: 2;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    }

    .item-name { font-weight: bold; color: #0000FF; font-size: 0.95em; }
    .item-qty { font-size: 1.3em; font-weight: bold; color: #000; margin: 3px 0; }
    .item-loc { color: #8DB48E; font-size: 0.85em; font-weight: bold; }
    
    /* 수량 0일 때 빨간색 */
    .out-of-stock { background-color: #FDF2F4; }
    .out-of-stock .item-qty { color: #FF0000; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">일 일 재 고 현 황 표</div>', unsafe_allow_html=True)

# 3. 데이터 로드 및 관리
if 'inventory_data' not in st.session_state:
    st.session_state.inventory_data = pd.DataFrame(columns=["품목명", "수량", "위치코드"])

st.subheader("📝 재고 데이터 입력")
edited_df = st.data_editor(
    st.session_state.inventory_data,
    num_rows="dynamic",
    use_container_width=True,
    hide_index=True
)

if st.button("수정 내용 적용하기"):

