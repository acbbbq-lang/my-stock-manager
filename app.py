import streamlit as st
import pandas as pd

# 1. 페이지 설정
st.set_page_config(page_title="일일 재고 현황표", layout="wide")

# 2. CSS: 간격 넓히기 및 시인성 최적화
st.markdown("""
<style>
    .title { text-align: center; font-size: 3.5em; font-weight: bold; text-decoration: underline; margin-bottom: 20px; }
    
    .main-container {
        position: relative; width: 1100px; margin: 0 auto; padding: 20px 0;
        background-color: white;
    }

    /* 행 간격: -80px에서 -45px로 줄여 위아래 간격을 벌림 */
    .row-cont { 
        display: flex; justify-content: center; position: relative; 
        margin-bottom: -45px; 
    }

    /* 레이어 순서 유지 */
    .layer-top { z-index: 100 !important; }
    .layer-bottom { z-index: 50 !important; }

    /* 카드 스타일: 좌우 간격(-15px -> -5px)을 벌려 글자 가림 방지 */
    .card {
        width: 135px; height: 135px;
        display: flex; flex-direction: column; justify-content: center; align-items: center;
        background-color: white; 
        margin: 0 -5px; 
        flex-shrink: 0;
        border: 2px solid #000; 
        box-shadow: 2px 2px 6px rgba(0,0,0,0.1);
    }

    .shape-circle { border-radius: 50%; }
    .shape-square { border-radius: 12px; }

    /* 텍스트 스타일: 가독성을 위해 크기 미세 조정 */
    .p-n { font-weight: bold; font-size: 14px; margin-bottom: 2px; }
    .p-q { font-size: 20px; font-weight: 900; color: #000; line-height: 1.1; }
    .p-l { color: #8eb44e; font-size: 12px; font-weight: bold; margin-top: 2px; }
    
    .t-blue { color: #0000FF; }
    .t-orange { color: #d35400; }
    .zero-bg { background-color: #fff1f0; } /* 수량 0일 때 배경색 */
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">일 일 재 고 현 황 표</div>', unsafe_allow_html=True)

# 3. 데이터 관리 (세션 상태)
if 'inven' not in st.session_state:
    st.session_state['inven'] = pd.DataFrame({
        "품목명": ["WASW", "WCRS", "WASW", "WASWP", "WUR", "WNS", "WASW"] + ["-"] * 28,
        "수량": [1508, 1671, 1754, 1496, 1494, 1686, 1500] + [0] * 28,
        "위치코드": ["A101", "A102", "A103", "A104", "A105", "A106", "A107"] + [f"A{i}" for i in range(201, 229)]
    })

# 4. 데이터 입력창 (상단 고정)
with st.expander("📝 데이터 수정 및 품목 입력"):
    edited_df = st.data_editor(st.session_state['inven'], use_container_width=True, num_rows="fixed")
    if st.button("내용 반영하기"):
        st.session_state['inven'] = edited_df
        st.rerun()

st.markdown("---") # 구분선

# 5. 현황판 배치
df = st.session_state['inven']
st.markdown('<div class="main-container">', unsafe_allow_html=True)

for r in range(5):
    is_circle = (r % 2 == 0)
    layer_cls = "layer-top" if is_circle else "layer-bottom"
    shape_cls = "shape-circle" if is_circle else "shape-square"
    
    # 지그재그 배치 간격 유지
    row_style = "margin-left: 70px;" if not is_circle else ""
    
    row_html = f'<div class="row-cont {layer_cls}" style="{row_style}">'
    
    sub_df = df.iloc[r*7 : (r+1)*7]
    for _, row in sub_df.iterrows():
        nm, lc, qt = str(row["품목명"]), str(row["위치코드"]), int(row["수량"])
        c_cls = "t-orange" if any(x in nm for x in ["WNS", "WCRS", "WUR"]) else "t-blue"
        bg_cls = "zero-bg" if qt == 0 else ""
        
        row_html += f'<div class="card {shape_cls} {bg_cls}">'
        row_html += f'<div class="p-n {c_cls}">{nm}</div>'
        row_html += f'<div class="p-q">{qt:,}</div>'
        row_html += f'<div class="p-l">{lc}</div></div>'
    
    row_html += '</div>'
    st.markdown(row_html, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
