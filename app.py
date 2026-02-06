import streamlit as st
import pandas as pd

# 1. 페이지 설정
st.set_page_config(page_title="일일 재고 현황표", layout="wide")

# 2. 도면 스타일 CSS (선과 격자 배경 포함)
st.markdown("""
<style>
    .title { text-align: center; font-size: 3em; font-weight: bold; text-decoration: underline; margin-bottom: 20px; font-family: 'serif'; }
    
    /* 전체 판 배경: 도면과 같은 선형 배경 구현 */
    .main-container {
        position: relative;
        width: 1100px;
        margin: 0 auto;
        padding: 50px 20px;
        background-color: white;
        border: 1px solid #ccc;
        overflow: hidden;
    }

    /* 뒷 배경 선 (격자 모양) */
    .bg-lines {
        position: absolute;
        top: 0; left: 0; width: 100%; height: 100%;
        z-index: 1;
        background-image: 
            linear-gradient(to bottom, transparent 115px, #333 115px, #333 116px, transparent 116px),
            linear-gradient(to bottom, transparent 245px, #333 245px, #333 246px, transparent 246px);
        background-size: 100% 100%;
    }

    .row-cont { 
        display: flex; 
        justify-content: center; 
        position: relative;
        z-index: 2;
        margin-bottom: -5px;
    }
    
    .zigzag-row { margin-left: 140px; }

    /* 개별 재고 카드 (동그라미) */
    .circle-card {
        border: 1.5px solid #000; border-radius: 50%; 
        width: 125px; height: 125px;
        display: flex; flex-direction: column; justify-content: center; align-items: center;
        background-color: white; margin: 5px; flex-shrink: 0;
        box-shadow: 1px 1px 3px rgba(0,0,0,0.2);
    }
    
    .p-name { font-weight: bold; color: #0000FF; font-size: 16px; margin-top: 5px; }
    .p-qty { font-size: 20px; font-weight: 900; color: #000; line-height: 1; margin: 2px 0; }
    .p-loc { color: #8eb44e; font-size: 14px; font-weight: bold; }
    
    /* 품목별 색상 강조 (WNS, WUR 등 도면 스타일) */
    .color-wns { color: #d35400 !important; } /* 주황색 */
    .color-loc-alt { color: #8eb44e; } /* 연두색 위치코드 */
    
    .zero-stock { background-color: #ffebee; }
    .zero-stock .p-qty { color: red; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">일 일 재 고 현 황 표</div>', unsafe_allow_html=True)

# 3. 데이터 초기화
if 'inven' not in st.session_state:
    st.session_state['inven'] = pd.DataFrame({
        "품목명": ["WASW", "WCRS", "WASW", "WASWP", "WUR", "WNS"] + [""] * 29,
        "수량": [1508, 1671, 1754, 1496, 1494, 1686] + [0] * 29,
        "위치코드": ["A101", "A102", "A103", "A104", "A105", "A106"] + [""] * 29
    })

# 4. 입력 표
with st.expander("📝 데이터 수정하기"):
    edited_df = st.data_editor(st.session_state['inven'], num_rows="fixed", use_container_width=True)
    if st.button("수정 내용 적용"):
        st.session_state['inven'] = edited_df
        st.rerun()

# 5. 도면형 현황판 출력
df = st.session_state['inven']
st.markdown('<div class="main-container"><div class="bg-lines"></div>', unsafe_allow_html
