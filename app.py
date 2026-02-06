import streamlit as st
import pandas as pd

# 1. 화면 설정
st.set_page_config(page_title="일일 재고 현황표", layout="wide")

# 2. 스타일 디자인
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
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">일 일 재 고 현 황 표</div>', unsafe_allow_html=True)

# 3. 데이터 관리
if 'inventory_data' not in st.session_state:
    st.session_state.inventory_data = pd.DataFrame(columns=["품목명", "수량"])

st.subheader("📝 재고 편집")

# 편집기 (괄호 에러 방지를 위해 설정 최소화)
edited_df = st.data_editor(
    st.session_state.inventory_data,
    num_rows="dynamic",
    use_container_width=True,
    hide_index=True
)

# 수정 적용 버튼
if st.button("수정 내용 적용하기"):
    if edited_df is not None:
        # 이름이 있는 행만 골라내기
        df_clean = edited_df.dropna(subset=["품목명"])
        df_clean = df_clean[df_clean["품목명"].astype(str).str.strip() != ""]
        st.session_state.inventory_data = df_clean
        st.rerun()

st.divider()

# 4. 현황판 출력
df = st
