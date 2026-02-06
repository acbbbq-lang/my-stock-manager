import streamlit as st
import pandas as pd

# 1. 페이지 설정
st.set_page_config(page_title="일일 재고 현황표", layout="wide")

# 2. CSS: 레이어 순서(z-index) 및 겹침 설정
st.markdown("""
<style>
    .title { text-align: center; font-size: 3.5em; font-weight: bold; text-decoration: underline; margin-bottom: 20px; }
    
    .main-container {
        position: relative; width: 1050px; margin: 0 auto; padding: 20px 0;
        background-color: white; min-height: 800px;
    }

    /* 배경 선 */
    .bg-lines {
        position: absolute; top: 0; left: 0; width: 100%; height: 100%; z-index: 1;
        background-image: 
            linear-gradient(to bottom, 
                transparent 100px, #000 100px, #000 101px, transparent 101px,
                transparent 240px, #000 240px, #000 241px, transparent 241px,
                transparent 380px, #000 380px, #000 381px, transparent 381px
            );
    }

    /* 행 간격: 음수 마진으로 위아래 겹침 */
    .row-cont { 
        display: flex; justify-content: center; position: relative; 
        margin-bottom: -55px; 
    }

    /* 동그라미 행(상단) vs 네모 행(하단) 레이어 순서 */
    .layer-top { z-index: 100 !important; }
    .layer-bottom { z-index: 50 !important; }

    /* 카드 스타일 */
    .card {
        width: 135px; height: 135px;
        display: flex; flex-direction: column; justify-content: center; align-items: center;
        background-color: white; margin: 0 -8px; flex-shrink: 0;
        border: 1.5px solid #000; box-shadow: 2px 2px 8px rgba(0,0,0,0.15);
    }

    .shape-circle { border-radius: 50%; }
    .shape-square { border-radius: 12px; }

    /* 텍스트 스타일 */
    .p-n { font-weight: bold; font-size: 15px; }
    .p-q { font-size: 21px; font-weight: 900; color: #000; margin: 1px 0; }
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

with st.expander("📝 데이터 편집기"):
    edited_df = st.data_editor(st.session_state['inven'], use_container_width=True)
    if st.button("수정 내용 적용"):
        st.session_state['inven'] = edited_df
        st.rerun()

# 4. 현황판 배치 (에러 수정 완료)
df = st.session_state['inven']
st.markdown('<div class="main-container"><div class="bg-lines"></div>', unsafe_allow_html=True)

for r in range(5):
    is_circle = (r % 2 == 0)
    layer_cls = "layer-top" if is_circle else "layer-bottom"
    shape_cls = "shape-circle" if is_circle else "shape-square"
    row_style = "margin-left: 70px;" if not is_circle else ""
    
    # f-string 시작
    row_html = f'<div class="row-cont {layer_cls}" style="{row_style}">'
    
    sub_df = df.iloc[r*7 : (r+1)*7]
    for _, row in sub_df.iterrows():
        nm, lc, qt = str(row["품목명"]), str(row["위치코드"]), int(row["수량"])
        c_cls = "t-orange" if any(x in nm for x in ["WNS", "WCRS", "WUR"]) else "t-blue"
        bg_cls = "zero-bg" if qt == 0 else ""
        
        # 카드 HTML을 row_html에 추가 (따옴표 짝 맞춤)
        row_html += f'<div class="card {shape_cls} {bg_cls}">'
        row_html += f'<div class="p-n {c_cls}">{nm}</div>'
        row_html += f'<div class="p-q">{qt:,}</div>'
        row_html += f'<div class="p-l">{lc}</div></div>'
    
    row_html += '</div>' # 행 닫기
    st.markdown(row_html, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
