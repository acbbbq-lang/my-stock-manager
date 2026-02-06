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
# 1행(예시 데이터)을 아예 비워둔 상태로 시작하게 설정했습니다.
if 'inventory_data' not in st.session_state:
    st.session_state.inventory_data = pd.DataFrame(columns=["item_name", "quantity", "location"])

st.subheader("📝 재고 편집 (수정 후 아래 버튼을 꼭 눌러주세요)")

# 표 편집기
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
    # 수정된 데이터를 세션에 저장하고 화면 새로고침
    st.session_state.inventory_data = edited_df.reset_index(drop=True)
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
            # 품목명이 비어있는 행은 건너뜁니다.
            if pd.isna(item['item_name']) or str(item['item_name']).strip() == "":
                continue
                
            with cols[j]:
                # 수량 에러 방지 처리
                try:
                    val = item['quantity']
                    qty_val = float(val) if pd.notnull(val) else 0.0
                except:
                    qty_val = 0.0
                
                is_low = "low-stock" if qty_val <= 0 else ""
                formatted_qty = f"{int(qty_val):,}"
                
                st.markdown(f"""
                    <div class="stock-card {is_low}">
                        <div class="item-name">{item['item_name']}</div>
                        <div class="item-qty">{formatted_qty}</div>
                        <div class="item-loc">{item['location'] if pd.notnull(item['location']) else '-'}</div>
                    </div>
                """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.info("위의 표에 재고 내용을 입력하고 '수정 내용 적용하기' 버튼을 눌러주세요.")
