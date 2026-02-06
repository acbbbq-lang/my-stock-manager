import streamlit as st
import pandas as pd

# 1. 페이지 설정 (가로로 넓게)
st.set_page_config(page_title="일일 재고 현황표", layout="wide")

# 2. 가로 배치 전용 CSS (절대 세로로 안 나오게 강제)
st.markdown("""
<style>
    .title { text-align: center; font-size: 3em; font-weight: bold; text-decoration: underline; margin-bottom: 30px; }
    .main-board { display: flex; flex-direction: column; align-items: center; width: 100%; }
    
    /* 한 줄(7개)을 가로로 묶어주는 컨테이너 */
    .row-cont { 
        display: flex; 
        flex-direction: row; 
        justify-content: center; 
        width: 100%; 
        margin-bottom: -45px; 
    }
    
    /* 지그재그 효과 (줄마다 엇갈림) */
    .zigzag { margin-left: 140px; } 

    .circle {
        border: 2px solid #333; border-radius: 50%; 
        width: 120px; height: 120px;
        display: flex; flex-direction: column; justify-content: center; align-items: center;
        background-color: white; margin: 8px; flex-shrink: 0;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    }
    .p-n { font-weight: bold; color: blue; font-size: 0.8em; text-align: center; }
    .p-q { font-size: 1.1em; font-weight: bold; color: black; margin: 2px 0; }
    .p-l { color: green; font-size: 0.7em; font-weight: bold; }
    
    /* 수량 0일 때 빨간색 배경 */
    .zero { background-color: #fff1f0; }
    .zero .p-q { color: red; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">일 일 재 고 현 황 표</div>', unsafe_allow_html=True)

# 3. 데이터 초기화 (35개 항목 강제 생성)
if 'inven' not in st.session_state:
    st.session_state['inven'] = pd.DataFrame({
        "품목명": [""] * 35, "수량": [0] * 35, "위치코드": [""] * 35
    })

# 4. 상단 입력 표 (무조건 노출)
st.subheader("📝 재고 데이터 입력 (35개 항목)")
edited_df = st.data_editor(st.session_state['inven'], num_rows="fixed", use_container_width=True)

if st.button("수정 내용 적용하기"):
    st.session_state['inven'] = edited_df
    st.rerun()

st.divider()

# 5. 하단 현황판 (동그라미 35개 가로 지그재그 출력)
df = st.session_state['inven']
