import streamlit as st
import pandas as pd

# 1. 페이지 설정
st.set_page_config(page_title="일일 재고 현황표", layout="wide")

# 2. CSS 설정 (z-index 추가하여 겹침 순서 조정)
st.markdown("""
<style>
    .title { text-align: center; font-size: 3.5em; font-weight: bold; text-decoration: underline; margin-bottom: 10px; font-family: 'serif'; }
    
    .main-container {
        position: relative; width: 1000px; margin: 0 auto; padding: 20px 0px;
        background-color: white; overflow: visible; /* 겹침을 위해 visible로 변경 */
    }

    /* 도면 뒷 배경 가로선 */
    .bg-lines {
        position: absolute; top: 0; left: 0; width: 100%; height: 100%; z-index: 0;
        background-image: 
            linear-gradient(to bottom, 
                transparent 70px, #000 70px, #000 71.5px, transparent 71.5px,
                transparent 180px, #000 180px, #000 181.5px, transparent 181.5px,
                transparent 290px, #000 290px, #000 291.5px, transparent 291.5px
            );
    }

    .row-cont { 
        display: flex; 
        justify-content: center; 
        position: relative; 
        margin-bottom: -50px; /* 위아래 겹침 강도 */
    }

    /* 카드 공통 스타일 */
    .card {
        width: 135px; height: 135px;
        display: flex; flex-direction: column; justify-content: center; align-items: center;
        background-color: white; 
        margin: 0 -8px; /* 좌우 겹침 */
        flex-shrink: 0;
        border: 1.5px solid #000;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    }

    /* 1, 3, 5행: 동그라미 (z-index를 높여서 위로 올림) */
    .row-circle { z-index: 10; }
    .shape-circle { border-radius: 50%; }

    /* 2, 4행: 네모 (z-index를 낮게 설정) */
    .row-square { z-index: 5; }
    .shape-square { border-radius: 12px; }

    /* 텍스트 스타일 */
    .p-n { font-weight: bold; font-size: 15px; margin-top: 5px; }
    .p-q { font-size: 19px; font-weight: 900; color: #000; margin: 0; }
    .p-l { color: #8eb44e; font-size: 13px; font-weight: bold; }
    
    .t-blue { color: #0000FF; }
    .t-orange { color: #d35400; }
    .zero-bg { background-color: #fff1f0; }
    .zero-bg .p-q { color: red; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">일 일 재 고 현 황 표</div>', unsafe_allow_html=True)

# 3. 데이터 초기화
if 'inven' not in st.session_state:
    st.session_state['inven'] = pd.DataFrame({
        "품목명": ["WASW", "WCRS", "WASW", "WASWP", "WUR", "WNS", "WASW"] + ["-"] * 28,
        "수량": [1508, 1671, 1754, 1496, 1494, 1686, 1500] + [0] * 28,
        "위치코드": ["A101", "A102", "A103", "A104", "A105", "A106", "A107"] + [f"A{i}" for i in range(201, 229)]
    })

# 4. 입력창
with st.expander("📝 데이터 수정"):
    edited_df = st.data_editor(st.session_state['inven'], use_container_width=True)
    if st.button("적용"):
        st.session_state['inven'] = edited_df
        st.rerun()

# 5. 출력부
df = st.session_state['inven']
st.markdown('<div class="main-container"><div class="bg-lines"></div>', unsafe_allow_html=True)
