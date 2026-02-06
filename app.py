import streamlit as st
import pandas as pd

# --- 화면 설정 ---
st.set_page_config(page_title="일일 재고 현황표", layout="wide")

# --- 디자인 스타일 (보내주신 이미지 재현) ---
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
if 'inventory_data' not in st.session_state:
    st.session_state.inventory_data = pd.DataFrame([
        {"item_name": "WASW", "quantity": 1508.0, "location": "A101"},
        {"item_name": "WCRS", "quantity": 1671.0, "location": "A102"}
    ])

st.subheader("📝 재고 편집 (수정 후 아래 버튼을 꼭 눌러주세요)")

# 표 편집기
edited_df = st.data_editor(
    st.session_state.inventory_data,
    num_rows="dynamic",
    use_container_width=True
)

# [수정 적용] 버튼
if st.button("수정 내용 적용하기"):
    st.session_state.inventory_data = edited_df.copy()
    st.rerun()

st.divider()

# --- 현황판 출력 ---
df = st.session_state.inventory_data

if not df.empty:
    st.markdown('<div class="stock-container">', unsafe_allow_html=True)
    
    # 6개씩 배치
    for i in range(0, len(df), 6):
        row_data = df.iloc[i:i+6]
        cols = st.columns(6)
        for j, (idx, item) in enumerate(row_data.iterrows()):
            with cols[j]:
                # --- 에러 방지 처리 시작 ---
                try:
                    raw_qty = item['quantity']
                    # 값이 비었거나 숫자가 아니면 0으로 처리
                    qty_val = float(raw_qty) if pd.notnull(raw_qty) else 0.0
                except:
                    qty_val = 0.0
                
                is_low = "low-stock" if qty_val <= 0 else ""
                formatted_qty = f"{int(qty_val):,}"
                # --- 에러 방지 처리 끝 ---
                
                st.markdown(f"""
                    <div class="stock-card {is_low}">
                        <div class="item-name">{item.get('item_name', '품목없음')}</div>
                        <div class="item-qty">{formatted_qty}</div>
                        <div class="item-loc">{item.get('location', '-')}</div>
                    </div>
                """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
