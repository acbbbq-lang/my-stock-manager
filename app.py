import streamlit as st
import pandas as pd

st.set_page_config(page_title="일일 재고 현황표", layout="wide")

# 디자인 설정
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
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="title">일 일 재 고 현 황 표</div>', unsafe_allow_html=True)

# 초기 데이터 (완전히 비워둠)
if 'inventory_data' not in st.session_state:
    st.session_state.inventory_data = pd.DataFrame(columns=["품목명", "수량"])

st.subheader("📝 재고 편집")

# 핵심 수정 부분: num_rows="dynamic"을 유지하되, 
# 사용자가 명확히 입력한 것만 관리하도록 로직 변경
edited_df = st.data_editor(
    st.session_state.inventory_data,
    num_rows="dynamic", # 줄 추가/삭제 가능
    use_container_width=True,
    hide_index=True # 왼쪽의 숫자(0, 1...) 숨기기
)

if st.button("수정 내용 적용하기"):
    # 품목명이나 수량 둘 중 하나라도 입력된 행만 필터링해서 저장
    filtered_df = edited_df.dropna(how='all').copy()
    # 품목명이 비어있는 행은 제외
    filtered_df = filtered_df[filtered_df["품목명"].astype(str).str.strip() != ""]
    st.session_state.inventory_data = filtered_df
    st.rerun()

st.divider()

# 현황판 출력
df = st.session_state.inventory_data

if not df.empty:
    st.markdown('<div class="stock-container">', unsafe_allow_html=True)
    for idx, item in df.iterrows():
        name = str(item["품목명"]).strip()
        try:
            qty = float(item["수량"]) if pd.notnull(item["수량"]) else 0.0
        except:
            qty = 0.0
            
        st.markdown(f"""
            <div class="stock-card">
                <div class="item-name">{name}</div>
                <div class


