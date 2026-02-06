import streamlit as st
import pandas as pd

# --- 화면 설정 ---
st.set_page_config(page_title="일일 재고 현황표", layout="wide")

# --- 디자인 스타일 ---
st.markdown("""
    <style>
    .title { text-align: center; font-size: 3em; font-weight: bold; text-decoration: underline; margin-bottom: 30px; }
    .stock-container { display: flex; flex-wrap: wrap; justify-content: center; background-color: white; padding: 20px; border: 1px solid #ccc; }
    .stock-card {
        border: 1px solid #333;
        border-radius: 50%;
        width: 120px;
        height: 120px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        margin: 10px;
        text-align: center;
        background-color: white;
    }
    .item-name { font-weight: bold; color: #0000FF; font-size: 1em; }
    .item-qty { font-size: 1.2em; font-weight: bold; margin: 2px 0; color: #000; }
    .item-loc { color: #88bb88; font-size: 0.8em; }
    .low-stock { background-color: #ffebee; border-color: #ff0000; }
    .low-stock .item-qty { color: #ff0000; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="title">일 일 재 고 현 황 표</div>', unsafe_allow_html=True)

# --- 데이터 관리 ---
# 1행 없이 빈 상태로 시작하도록 설정
if 'inventory_data' not in st.session_state:
    st.session_state.inventory_data = pd.DataFrame(columns=["item_name", "quantity", "location"])

st.subheader("📝 재고 편집 (수정 후 아래 버튼을 꼭 눌러주세요)")

# 표 편집기 (괄호 닫기 오류 수정 완료)
edited_df = st.data_editor(
    st.session_state.inventory_data,
    num_rows="dynamic",
    use_container_width=True,
    column_config={
        "item_name": "품목명",
        "quantity": "수량",
        "location": "위치코드"
    }
)

# [수정 적용] 버튼
if st.button("수정 내용 적용하기"):
    st.session_state.inventory_data = edited_df.reset_index(drop=True)
    st.rerun()

st.divider()

# --- 현황판 출력 ---
df = st.session_state.
