import streamlit as st
import pandas as pd

# 1. 페이지 설정
st.set_page_config(page_title="일일 재고 현황표", layout="wide")

# 2. CSS: 동그라미 6개 기준 중앙 정렬 및 겹침 최적화
st.markdown("""
<style>
    .title { text-align: center; font-size: 3em; font-weight: bold; text-decoration: underline; margin-bottom: 20px; }
    
    .main-container {
        display: flex; flex-direction: column; align-items: center; width: 100%;
    }

    .row-cont { 
        display: flex; 
        justify-content: center; /* 행 전체 중앙 정렬 */
        width: 100%; 
        margin-bottom: -55px; /* 상하 밀착 */
        position: relative;
    }

    /* 레이어 순서 */
    .layer-top { z-index: 100; }
    .layer-bottom { z-index: 50; }

    /* 카드 스타일 */
    .card {
        width: 130px; height: 130px;
        display: flex; flex-direction: column; justify-content: center; align-items: center;
        background-color: white; border: 2px solid #000;
        margin: 0 -5px; /* 좌우 밀착 */
        flex-shrink: 0;
        box-shadow: 1px 1px 4px rgba(0,0,0,0.1);
    }

    .shape-circle { border-radius: 50%; }
    .shape-square { border-radius: 15px; }

    /* 텍스트 가독성 */
    .p-n { font-weight: bold; font-size: 13px; margin-bottom: 2px; }
    .p-q { font-size: 19px; font-weight: 900; color: #000; line-height: 1.0; }
    .p-l { color: #8eb44e; font-size: 11px; font-weight: bold; margin-top: 2px; }
    
    .t-blue { color: #0000FF; }
    .t-orange { color: #d35400; }
    .zero-bg { background-color: #fff1f0; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">일 일 재 고 현 황 표</div>', unsafe_allow_html=True)

# 3. 데이터 로드 (6개/7개 교차 배치를 위한 데이터 구조)
if 'inven' not in st.session_state:
    # 5행 기준 (6+7+6+7+6 = 총 32개 항목 필요)
    total_needed = 32
    st.session_state['inven'] = pd.DataFrame({
        "품목명": ["WASW", "WCRS", "WASW", "WASWP", "WUR", "WNS"] + ["-"] * (total_needed - 6),
        "수량": [1508, 1671, 1754, 1496, 1494, 1686] + [0] * (total_needed - 6),
        "위치코드": [f"A{i}" for i in range(101, 101 + total_needed)]
    })

with st.expander("📝 데이터 관리 (수정 후 저장 버튼을 누르세요)"):
    edited_df = st.data_editor(st.session_state['inven'], use_container_width=True)
    if st.button("저장 및 새로고침"):
        st.session_state['inven'] = edited_df
        st.rerun()

# 4. 현황판 출력
df = st.session_state['inven']
full_html = '<div class="main-container">'

current_idx = 0
for r in range(5):
    is_circle = (r % 2 == 0)
    layer_cls = "layer-top" if is_circle else "layer-bottom"
    shape_cls = "shape-circle" if is_circle else "shape-square"
    
    # 동그라미 행은 6개, 네모 행은 7개씩 가져오기
    count = 6 if is_circle else 7
    
    full_html += f'<div class="row-cont {layer_cls}">'
    
    sub_df = df.iloc[current_idx : current_idx + count]
    for _, row in sub_df.iterrows():
        nm, lc, qt = str(row["품목명"]), str(row["위치코드"]), int(row["수량"])
        c_cls = "t-orange" if any(x in nm for x in ["WNS", "WCRS", "WUR"]) else "t-blue"
        bg_cls = "zero-bg" if qt == 0 else ""
        
        card_tag = f'<div class="card {shape_cls} {bg_cls}"><div class="p-n {c_cls}">{nm}</div><div class="p-q">{qt:,}</div><div class="p-l">{lc}</div></div>'
        full_html += card_tag
        
    full_html += '</div>'
    current_idx += count

full_html += '</div>'
st.markdown(full_html, unsafe_allow_html=True)
