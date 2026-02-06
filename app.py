import streamlit as st
import pandas as pd

# 1. 설정 및 디자인 (가로 배치 핵심 CSS)
st.set_page_config(page_title="일일 재고 현황표", layout="wide")
st.markdown("""
<style>
    .title { text-align: center; font-size: 3em; font-weight: bold; text-decoration: underline; margin-bottom: 30px; }
    .board { display: flex; flex-direction: column; align-items: center; width: 100%; }
    .row-cont { display: flex; justify-content: center; width: 100%; margin-bottom: -45px; }
    .zigzag { margin-left: 140px; } 
    .circle {
        border: 2px solid #333; border-radius: 50%; width: 130px; height: 130px;
        display: flex; flex-direction: column; justify-content: center; align-items: center;
        background-color: white; margin: 10px; flex-shrink: 0; box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    }
    .p-n { font-weight: bold; color: blue; font-size: 0.9em; text-align: center; }
    .p-q { font-size: 1.2em; font-weight: bold; color: black; margin: 2px 0; }
    .p-l { color: green; font-size: 0.8em; font-weight: bold; }
    .zero { background-color: #fff1f0; }
    .zero .p-q { color: red; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">일 일 재 고 현 황 표</div>', unsafe_allow_html=True)

# 2. 데이터 초기화 (35개 항목)
if 'inven' not in st.session_state:
    st.session_state['inven'] = pd.DataFrame({
        "품목명": [""] * 35, "수량": [0] * 35, "위치코드": [""] * 35
    })

# 3. 입력 표
st.subheader("📝 재고 데이터 입력 (35개 항목)")
edited_df = st.data_editor(st.session_state['inven'], num_rows="fixed", use_container_width=True)

if st.button("수정 내용 적용하기"):
    st.session_state['inven'] = edited_df
    st.rerun()

st
