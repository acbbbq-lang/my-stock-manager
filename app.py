import streamlit as st
import pandas as pd

# 1. 페이지 설정
st.set_page_config(page_title="일일 재고 현황표", layout="wide")

# 2. 디자인 스타일
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

# 3. 데이터 초기화
if 'inventory_data' not in st.session_state:
    st.session_state.inventory_data = pd.DataFrame(columns=["품목명", "수량"])

st.subheader("📝 재고 편집")

# 4. 재고 입력 표
edited_df = st.data_editor(
    st.session_state.inventory_data,
    num_rows="dynamic",
    use_container_width=True,
    hide_index=True
)

# 5. 적용 버튼 (41번 줄 에러 구간 수정 완료)
if st.button("수정 내용 적용하기"):
    if edited_df is not None:
        # 에러가 났던 부분을 아주 안전한 방식으로 교체했습니다.
        df_temp = edited_df.copy()
        # 품목명이 비어있지 않은 데이터만 골라내기
        st.session_state.inventory_data = df_temp[df_temp["품목명"].fillna("").str.strip() != ""]
        st.rerun()

st.divider()

# 6. 현황

