import streamlit as st
import pandas as pd

# 1. 화면 설정
st.set_page_config(page_title="일일 재고 현황표", layout="wide")

# 2. 디자인 스타일 (동그라미 카드 설정)
st.markdown("""
    <style>
    .title { text-align: center; font-size: 3em; font-weight: bold; text-decoration: underline; margin-bottom: 30px; }
    .stock-container { display: flex; flex-wrap: wrap; justify-content: center; background-color: white; padding: 20px; border: 1px solid #ccc; min-height: 200px; }
    .stock-card {
        border: 1px solid #333; border-radius: 50%; width: 120px; height: 120px;
        display: flex; flex-direction: column; justify-content: center; align-items: center;
        margin: 10px; text-align: center; background-color: white;
    }
    .item-name { font-weight: bold; color: #0000FF; font-size: 0.9em; }
    .item-qty { font-size: 1.2em; font-weight: bold; margin: 2px 0; color: #000; }
    .item-loc { color: #88bb88; font-size: 0.8em; }
    .low-stock { background-color: #ffebee; border-color: #ff0000; }
    .low-stock .item-qty { color: #ff0000; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="title">일 일 재 고 현 황 표</div>', unsafe_allow_html=True)

# 3. 데이터 초기화 (빈 표로 시작)
if 'inventory_data' not in st.session_state:
    st.session_state.inventory_data = pd.DataFrame(columns=["item_name", "quantity", "location"])

# 4. 데이터 편집기
st.subheader("📝 재고 편집 (수정 후 아래 버튼 클릭)")
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

# 5. 수정 버튼 클릭 시 데이터 저장
if st.button("수정 내용 적용하기"):
    st.session_state.inventory_data = edited_df.copy()
    st.success("데이터가 반영되었습니다! 아래 현황표를 확인하세요.")
    st.rerun()

st.divider()

# 6. 현황판 출력 (데이터가 있을 때만 출력)
df = st.session_state.inventory_data

if not df.empty:
    st.markdown('<div class="stock-container">', unsafe_allow_html=True)
    # 한 줄에 6개씩 배치하기 위한 로직
    for i in range(0, len(df), 6):
        row_data = df.iloc[i:i+6]
        cols = st.columns(6)
        for j, (idx, item) in enumerate(row_data.iterrows()):
            # 품목명이 있는 경우에만 동그라미를 그립니다.
            if pd.notnull(item['item_name']) and str(item['item_name']).strip() != "":
                with cols[j]:
                    try:
                        qty = float(item['quantity']) if pd.notnull(item['quantity']) else 0.0
                    except:
                        qty = 0.0
                    
                    is_low = "low-stock" if qty <= 0 else ""
                    
                    st.markdown(f"""
                        <div class="stock-card {is_low}">
                            <div class="item-name">{item['item_name']}</div>
                            <div class="item-qty">{int(qty):,}</div>
                            <div class="item-loc">{
