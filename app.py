import streamlit as st
import pandas as pd

# 1. 화면 설정 및 디자인
st.set_page_config(page_title="일일 재고 현황표", layout="wide")

st.markdown("""
    <style>
    .title { text-align: center; font-size: 3em; font-weight: bold; text-decoration: underline; margin-bottom: 30px; }
    .stock-container { display: flex; flex-wrap: wrap; justify-content: center; background-color: white; padding: 20px; border: 1px solid #ccc; }
    .stock-card {
        border: 1px solid #333; border-radius: 50%; width: 120px; height: 120px;
        display: flex; flex-direction: column; justify-content: center; align-items: center;
        margin: 10px; text-align: center; background-color: white;
    }
    .item-name { font-weight: bold; color: #0000FF; font-size: 1em; }
    .item-qty { font-size: 1.2em; font-weight: bold; margin: 2px 0; color: #000; }
    .item-loc { color: #88bb88; font-size: 0.8em; }
    .low-stock { background-color: #ffebee; border-color: #ff0000; }
    .low-stock .item-qty { color: #ff0000; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="title">일 일 재 고 현 황 표</div>', unsafe_allow_html=True)

# 2. 데이터 초기화
if 'inventory_data' not in st.session_state:
    st.session_state.inventory_data = pd.DataFrame(columns=["item_name", "quantity", "location"])

# 3. 데이터 입력/수정 표
st.subheader("📝 재고 편집 (수정 후 아래 버튼 클릭)")
edited_df = st.data_editor(
    st.session_state.inventory_data,
    num_rows="dynamic",
    use_container_width=True,
    column_config={"item_name": "품목명", "quantity": "수량", "location": "위치코드"}
)

if st.button("수정 내용 적용하기"):
    st.session_state.inventory_data = edited_df.reset_index(drop=True)
    st.rerun()

st.divider()

# 4. 동그란 현황판 출력
df = st.session_state.inventory_data

if not df.empty:
    st.markdown('<div class="stock-container">', unsafe_allow_html=True)
    # 6개씩 묶어서 처리
    for i in range(0, len(df), 6):
        row_data = df.iloc[i:i+6]
        cols = st.columns(6)
        # enumerate 안의 모든 괄호 짝을 맞췄습니다.
        for j, (idx, item) in enumerate(row_data.iterrows()):
            if pd.isna(item['item_name']) or str(item['item_name']).strip() == "":
                continue
            with cols[j]:
                try:
                    qty_val = float(item['quantity']) if pd.notnull(item['quantity']) else 0.0
                except:
                    qty_val = 0.
