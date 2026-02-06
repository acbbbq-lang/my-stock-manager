import streamlit as st
import pandas as pd

# 1. 화면 설정
st.set_page_config(page_title="재고 현황표", layout="wide")

# 2. 디자인 스타일 (동그라미 카드)
st.markdown("""
<style>
    .title { text-align: center; font-size: 3em; font-weight: bold; text-decoration: underline; margin-bottom: 30px; }
    .stock-container { display: flex; flex-wrap: wrap; justify-content: center; background-color: white; padding: 20px; border: 1px solid #ccc; min-height: 200px; }
    .stock-card {
        border: 1px solid #333; border-radius: 50%; width: 130px; height: 130px;
        display: flex; flex-direction: column; justify-content: center; align-items: center;
        margin: 15px; text-align: center; background-color: white;
    }
    .item-name { font-weight: bold; color: #0000FF; font-size: 0.9em; margin-bottom: 5px; }
    .item-qty { font-size: 1.3em; font-weight: bold; color: #000; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">일 일 재 고 현 황 표</div>', unsafe_allow_html=True)

# 3. 데이터 관리 (아이템명, 수량만 사용)
if 'inventory_data' not in st.session_state:
    st.session_state.inventory_data = pd.DataFrame(columns=["품목명", "수량"])

st.subheader("📝 재고 편집")

# 4. 데이터 입력기
edited_df = st.data_editor(
    st.session_state.inventory_data,
    num_rows="dynamic",
    use_container_width=True,
    hide_index=True
)

# 5. 수정 내용 적용 버튼
if st.button("수정 내용 적용하기"):
    if edited_df is not None:
        # 품목명이 비어있지 않은 데이터만 필터링
        df_new = edited_df.dropna(subset=["품목명"]).copy()
        df_new = df_new[df_new["품목명"].astype(str).str.strip() != ""]
        st.session_state.inventory_data = df_new.reset_index(drop=True)
        st.rerun()

st.divider()

# 6. 현황판 출력 (이 부분이 살아있어야 표가 뜹니다!)
df = st.session_state.inventory_data

if not df.empty:
    st.markdown('<div class="stock-container">', unsafe_allow_html=True)
    for _, item in df.iterrows():
        name = str(item["품목명"]).strip()
        try:
            qty_val = int(float(item["수량"])) if pd.notnull(item["수량"]) else 0
        except:
            qty_val = 0
            
        # 가장 안전한 방식의 HTML 출력
        card_html = f'<div class="stock-card">'
        card_html += f'<div class="item-name">{name}</div>'
        card_html += f'<div class="item-qty">{qty_val:,}</div>'
        card_html += '</div>'
        st.markdown(card_html, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.info("입력된 재고가 없습니다. 위 표에 품목명과 수량을 입력하고 버튼을 눌러주세요.")
