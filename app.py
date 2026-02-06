import streamlit as st
import pandas as pd

# 1. 화면 설정
st.set_page_config(page_title="일일 재고 현황표", layout="wide")

# 2. 스타일 설정 (동그란 카드 디자인)
st.markdown("""
    <style>
    .title { text-align: center; font-size: 3em; font-weight: bold; text-decoration: underline; margin-bottom: 30px; }
    .stock-container { display: flex; flex-wrap: wrap; justify-content: center; background-color: white; padding: 20px; border: 1px solid #ccc; }
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

# 3. 데이터 초기화
if 'inventory_data' not in st.session_state:
    st.session_state.inventory_data = pd.DataFrame(columns=["item_name", "quantity", "location"])

# 4. 데이터 편집기 (문제가 된 33번 줄 괄호 완벽 수정)
st.subheader("📝 재고 편집")
edited_df = st.data_editor(
    st.session_state.inventory_data,
    num_rows="dynamic",
    use_container_width=True
)

# 5. 적용 버튼
if st.button("수정 내용 적용하기"):
    st.session_state.inventory_data = edited_df.copy()
    st.rerun()

st.divider()

# 6. 현황판 출력
df = st.session_state.inventory_data

if not df.empty:
    st.markdown('<div class="stock-container">', unsafe_allow_html=True)
    for i in range(0, len(df), 6):
        row_data = df.iloc[i:i+6]
        cols = st.columns(6)
        for j, (idx, item) in enumerate(row_data.iterrows()):
            name = str(item['item_name']).strip() if pd.notnull(item['item_name']) else ""
            if name != "":
                with cols[j]:
                    try:
                        qty = float(item['quantity']) if pd.notnull(item['quantity']) else 0.0
                    except:
                        qty = 0.0
                    loc = str(item['location']) if pd.notnull(item['location']) else "-"
                    is_low = "low-stock" if qty <= 0 else ""
                    
                    st.markdown(f"""
                        <div class="stock-card {is_low}">
                            <div class="item-name">{name}</div>
                            <div class="item-qty">{int(qty):,}</div>
                            <div class="item-loc">{loc}</div>
                        </div>
                    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.warning("데이터가 없습니다. 위 표에 재고를 입력하고 버튼을 눌러주세요.")

