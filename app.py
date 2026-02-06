import streamlit as st
import pandas as pd

# 1. 페이지 설정
st.set_page_config(page_title="일일 재고 현황표", layout="wide")

# 2. CSS: 중간의 불필요한 선을 없애고 겹침을 최적화
st.markdown("""
<style>
    .title { text-align: center; font-size: 3.5em; font-weight: bold; text-decoration: underline; margin-bottom: 20px; }
    
    /* 메인 컨테이너: 배경 선 제거 및 깔끔한 흰색 배경 */
    .main-container {
        position: relative; width: 1000px; margin: 0 auto; padding: 20px 0;
        background-color: white; min-height: 700px;
    }

    /* 행 간격: 중간에 틈이 없도록 음수 마진을 더 강하게 설정 */
    .row-cont { 
        display: flex; justify-content: center; position: relative; 
        margin-bottom: -65px; /* 위아래 카드를 더 밀착시킴 */
    }

    /* 동그라미 행(상단 레이어) */
    .layer-top { z-index: 100 !important; }
    /* 네모 행(하단 레이어) */
    .layer-bottom { z-index: 50 !important; }

    /* 카드 기본 스타일 */
    .card {
        width: 135px; height: 135px;
        display: flex; flex-direction: column; justify-content: center; align-items: center;
        background-color: white; margin: 0 -12px; flex-shrink: 0;
        border: 2px solid #000; box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
    }

    .shape-circle { border-radius: 50%; }
    .shape-square { border-radius: 12px; }

    /* 텍스트 스타일 */
    .p-n { font-weight: bold; font-size: 15px; }
    .p-q { font-size: 21px; font-weight: 900; color: #000; margin: 2px 0; }
    .p-l { color: #8eb44e; font-size: 13px; font-weight: bold; }
    
    .t-blue { color: #0000FF; }
    .t-orange { color: #d35400; }
    .zero-bg { background-color: #fff1f0; }
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

# 4. 현황판 출력
df = st.session_state['inven']
# 불필요한 bg-lines를 제거한 컨테이너 시작
st.markdown('<div class="main-container">', unsafe_allow_html=True)

for r in range(5):
    is_circle = (r % 2 == 0)
    layer_cls = "layer-top" if is_circle else "layer-bottom"
    shape_cls = "shape-circle" if is_circle else "shape-square"
    
    # 지그재그 배치: 네모 행을 오른쪽으로 절반 정도 밀어넣음
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
