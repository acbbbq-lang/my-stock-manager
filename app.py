import streamlit as st
import pandas as pd

# 1. 페이지 설정 (반드시 코드 최상단에 있어야 함)
st.set_page_config(page_title="일일 재고 현황표", layout="wide")

# 2. 디자인 스타일 (지그재그 가로 배치 및 색상)
st.markdown("""
<style>
    .title { text-align: center; font-size: 3.5em; font-weight: bold; text-decoration: underline; margin-bottom: 40px; }
    .board-container { display: flex; flex-direction: column; align-items: center; width: 100%; padding: 20px; }
    
    /* 가로 배치를 위한 설정 */
    .stock-row { display: flex; flex-direction: row; justify-content: center; width: 100%; margin-bottom: -45px; }
    .row-offset { margin-left: 140px; } /* 지그재그 밀기 효과 */
    
    .stock-card {
        border: 1.5px solid #333; border-radius: 50%; width: 130px; height: 130px;
        display: flex; flex-direction: column; justify-content: center; align-items: center;
        background-color: white; margin: 10px; z-index: 2;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    }
    .item-name { font-weight: bold; color: #0000FF; font-size: 0.95em; }
    .item-qty { font-size: 1.3em; font-weight: bold; color: #000; margin: 3px 0; }
    .item-loc { color: #8DB48E; font-size: 0.85em; font-weight: bold; }
    
    /* 수량 0일 때 스타일 */
    .out-of-stock { background-color: #FDF2F4; border-color: #FFB6C1; }
    .out-of-stock .item-qty { color: #FF0000; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">일 일 재 고 현 황 표</div>', unsafe_allow_html=True)

# 3. 데이터 초기화 (변수명 inventory_data로 통일)
if 'inventory_data' not in st.session_state:
    st.session_state['inventory_data'] = pd.DataFrame(columns=["품목명", "수량", "위치코드"])

# 4. 데이터 입력 섹션 (이게 사라졌던 부분입니다!)
st.subheader("📝 재고 데이터 입력")
# 괄호를 확실히 닫았습니다.
edited_df = st.data_editor(
    st.session_state['inventory_data'],
    num_rows="dynamic",
    use_container_width=True,
    hide_index=True,
    key="inventory_editor"
)

# 수정 내용 적용 버튼
if st.button("수정 내용 적용하기"):
    if edited_df is not None:
        # 품목명이 있는 데이터만 필터링 (빈 줄 제거)
        df_new = edited_df.

