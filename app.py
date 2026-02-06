import streamlit as st
import pandas as pd

# 1. 페이지 설정
st.set_page_config(page_title="일일 재고 현황표", layout="wide")

# 2. 디자인 스타일 (지그재그 가로 배치 강제 설정)
st.markdown("""
<style>
    .title { text-align: center; font-size: 3.5em; font-weight: bold; text-decoration: underline; margin-bottom: 40px; }
    .board-container { display: flex; flex-direction: column; align-items: center; width: 100%; padding: 20px; background-color: white; }
    
    /* 가로 배치를 위한 레이아웃 */
    .stock-row { display: flex; flex-direction: row; justify-content: center; width: 100%; margin-bottom: -45px; }
    .row-offset { margin-left: 140px; } /* 지그재그 효과 */
    
    .stock-card {
        border: 1.5px solid #333; border-radius: 50%; width: 130px; height: 130px;
        display: flex; flex-direction: column; justify-content: center; align-items: center;
        background-color: white; margin: 10px; z-index: 2;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    }
    .item-name { font-weight: bold; color: #0000FF; font-size: 0.9em; text-align: center; }
    .item-qty { font-size: 1.2em; font-weight: bold; color: #000; margin: 2px 0; }
    .item-loc { color: #8DB48E; font-size: 0.8em; font-weight: bold; }
    
    /* 수량 0 또는 비어있을 때 스타일 */
    .out-of-stock { background-color: #FDF2F4; }
    .out-of-stock .item-qty { color: #FF0000; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">일 일 재 고 현 황 표</div>', unsafe_allow_html=True)

# 3. 데이터 초기화 (35개 빈 칸 생성)
if 'inventory_data' not in st.session_state:
    st.session_state['inventory_data'] = pd.DataFrame({
        "품목명": [""] * 35, 
        "수량": [None] * 35, 
        "위치코드": [""] * 35
    })

# 4. 데이터 입력 표 (이 부분은 이제 항상 뜹니다)
st.subheader("📝 재고 데이터 입력 (35개 항목)")
edited_df = st.data_editor(
    st.session_state['inventory_data'],
    num_rows="fixed", # 35개 행 고정
    use_container_width=True,
    hide_index=False,
    key="inventory_editor"
)

# [수정 내용 적용하기] 버튼
if st.button("수정 내용 적용하기"):
    if edited_df is not None:
        st.session_state['inventory_data'] = edited_df.copy()
        st.rerun()

st.divider()

# 5. 현황판 출력 (7개씩 5줄 = 35개 지그재그 배치)
df = st.session_state['inventory_data']

st.markdown('<div class="board-container">', unsafe_allow_html=True)

# 35개를 7개씩 5줄로 출력
for i in range(0, 35, 7):
    row_num = i // 7
    # 홀수 번째 줄(1, 3줄)에 지그재그 밀기 적용
    offset_class = "row-offset" if row_num % 2 != 0 else ""
    st.markdown(f'<div class="stock-row {offset_class}">', unsafe_allow_html=True)
    
    row_items = df
