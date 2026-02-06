import streamlit as st
import pandas as pd
from io import StringIO

# 1. 페이지 설정
st.set_page_config(page_title="일일 재고 현황표", layout="wide")

# 2. CSS: 네모 확대 및 위아래 밀착 배치
st.markdown("""
<style>
    .title { text-align: center; font-size: 3em; font-weight: bold; text-decoration: underline; margin-bottom: 20px; }
    
    .main-container {
        display: flex; flex-direction: column; align-items: center; width: 100%;
    }

    .row-cont { 
        display: flex; 
        justify-content: center; 
        width: 100%; 
        /* 네모가 커진 만큼 겹침 정도를 강화하여 공백 제거 */
        margin-bottom: -85px; 
        position: relative;
    }

    .row-cont:last-child { margin-bottom: 100px; }

    .layer-top { z-index: 100; }
    .layer-bottom { z-index: 50; }

    /* 공통 카드 스타일 */
    .card {
        display: flex; flex-direction: column; justify-content: center; align-items: center;
        background-color: white; border: 2.5px solid #000;
        margin: 0 -8px; flex-shrink: 0;
        box-shadow: 2px 2px 6px rgba(0,0,0,0.1);
    }

    /* 동그라미: 기존 유지 */
    .shape-circle { width: 130px; height: 130px; border-radius: 50%; }

    /* 네모: 크기 확대 및 공백 제거를 위한 높이 조정 */
    .shape-square { 
        width: 190px; height: 170px; 
        border-radius: 10px; 
        background-color: #fcfcfc;
    }

    /* 텍스트 스타일 */
    .p-n { font-weight: bold; font-size: 16px; margin-bottom: 4px; }
    .p-q { font-size: 26px; font-weight: 900; color: #000; line-height: 1.0; }
    .p-l { color: #8eb44e; font-size: 14px; font-weight: bold; margin-top: 4px; }
    
    .t-blue { color: #0000FF; }
    .t-orange { color: #d35400; }
    .zero-bg { background-color: #fff1f0; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">일 일 재 고 현 황 표</div>', unsafe_allow_html=True)

# 3. 데이터 로직 (초기 데이터)
if 'inven' not in st.session_state:
    st.session_state['inven'] = pd.DataFrame({
        "품목명": ["WASW", "WCRS", "WASW", "WASWP", "WUR", "WNS"] + ["-"] * 29,
        "수량": [1508, 1671, 1754, 1496, 1494, 1686] + [0] * 29,
        "위치코드": [f"A{i}" for i in range(101, 136)]
    })

# --- 엑셀 복사 붙여넣기 섹션 ---
with st.expander("📋 엑셀 데이터 붙여넣기 (클릭)"):
    st.info("엑셀에서 3개 열(품목명, 수량, 위치코드)을 복사해서 아래 칸에 붙여넣으세요.")
    paste_data = st.text_area("엑셀 데이터를 여기에 붙여넣기 (Ctrl+V)", height=150)
    
    if st.button("붙여넣은 데이터 적용"):
        if paste_data:
            try:
                # 탭(Tab)으로 구분된 데이터를 읽어옴 (엑셀 복사 시 기본 형식)
                new_df = pd.read_csv(StringIO(paste_data), sep='\t', names=["품목명", "수량", "위치코드"])
                # 데이터가 35개보다 부족하면 채워줌
                if len(new_df) < 35:
                    extra = pd.DataFrame([["-", 0, "-"]] * (35 - len(new_df)), columns=["품목명", "수량", "위치코드"])
                    new_df = pd.concat([new_df, extra], ignore_index=True)
                
                st.session_state['inven'] = new_df.head(35)
                st.success("데이터가 성공적으로 반영되었습니다!")
                st.rerun()
            except Exception as e:
                st.error("데이터 형식이 맞지 않습니다. 3개의 열을 복사했는지 확인해주세요.")

# 직접 수정용 데이터 에디터
with st.expander("📝 개별 데이터 관리 (직접 수정)"):
    edited_df = st.data_editor(st.session_state['inven'], use_container_width=True)
    if st.button("수정사항 저장"):
        st.session_state['inven'] = edited_df
        st.rerun()

# 4. 현황판 출력
df = st.session_state['inven']
full_html = '<div class="main-
