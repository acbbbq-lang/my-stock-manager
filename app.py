import streamlit as st
import pandas as pd

# 1. 페이지 설정
st.set_page_config(page_title="일일 재고 현황표", layout="wide")

# 2. CSS (지그재그 가로 배치 디자인)
st.markdown("""
<style>
    .title { text-align: center; font-size: 3em; font-weight: bold; text-decoration: underline; margin-bottom: 30px; }
    .board { display: flex; flex-direction: column; align-items: center; width: 100%; }
    .stock-row { display: flex; flex-direction: row; justify-content: center; width: 100%; margin-bottom: -45px; }
    .row-offset { margin-left: 140px; }
    .stock-card {
        border: 2px solid #333; border-radius: 50%; width: 130px; height: 130px;
        display: flex; flex-direction: column; justify-content: center; align-items: center;
        background-color: white; margin: 10px; z-index: 2;
    }
    .item-name { font-weight: bold; color: blue; font-size: 0.9em; }
    .item-qty { font-size: 1.2em; font-weight: bold; color: black; }
    .item-loc { color: green; font-size: 0.8em; font-weight: bold; }
    .zero-qty { background-color: #ffebee; }
    .zero-qty .item-qty { color: red; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">일 일 재 고 현 황 표</div>', unsafe_allow_html=True)

# 3. 데이터 초기화 (35개 행 강제 생성)
if 'inven' not in st.session_state:
    st.session_state['inven'] = pd.DataFrame({
        "품목명": [""] * 35, "수량": [0] * 35, "위치코드": [""] * 35
    })

# 4. 상단 입력 표 (무조건 노출)
st.subheader("📝 재고 데이터 입력 (35개 항목)")
# 에러가 났던 rerun 부분을 안전하게 처리
edited_df = st.data_editor(st.session_state['inven'], num_rows="fixed", use_container_width=True)

if st.button("수정 내용 적용하기"):
    st.session_state['inven'] = edited_df
    st.rerun()  # <--- 이 부분이 잘리지 않게 주의하세요!

st.divider()

# 5. 하단 현황판 (지그재그 35개 출력)
df = st.session_state['inven']
st.markdown('<div class="board">', unsafe_allow_html=True)

for i in range(0, 35, 7):
    # 7개씩 끊어서 줄 생성 (홀수줄 밀기)
    is_offset = "row-offset" if (i // 7) % 2 != 0 else ""
    st.markdown(f'<div class="stock-row {is_offset}">', unsafe_allow_html=True)
