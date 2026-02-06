import streamlit as st
import pandas as pd

# 1. 페이지 설정
st.set_page_config(page_title="일일 재고 현황표", layout="wide")

# 2. 겹침 레이아웃 전용 CSS
st.markdown("""
<style>
    .title { text-align: center; font-size: 3.5em; font-weight: bold; text-decoration: underline; margin-bottom: 10px; font-family: 'serif'; }
    
    .main-container {
        position: relative; width: 1000px; margin: 0 auto; padding: 20px 0px;
        background-color: white; overflow: hidden;
    }

    /* 도면 뒷 배경 가로선 */
    .bg-lines {
        position: absolute; top: 0; left: 0; width: 100%; height: 100%; z-index: 1;
        background-image: 
            linear-gradient(to bottom, 
                transparent 70px, #000 70px, #000 71.5px, transparent 71.5px,
                transparent 180px, #000 180px, #000 181.5px, transparent 181.5px,
                transparent 290px, #000 290px, #000 291.5px, transparent 291.5px
            );
    }

    /* 행 간격을 음수로 주어 위아래가 겹치게 설정 */
    .row-cont { 
        display: flex; 
        justify-content: center; 
        position: relative; 
        z-index: 2; 
        margin-bottom: -40px; /* 위아래 카드가 겹치도록 음수 마진 */
    }

    /* 카드 공통 스타일 (크기를 살짝 키워 겹침 효과 극대화) */
    .card {
        width: 135px; height: 135px;
        display: flex; flex-direction: column; justify-content: center; align-items: center;
        background-color: white; 
        margin: 0 -5px; /* 좌우 카드가 서로 겹치도록 음수 마진 */
        flex-shrink: 0;
        border: 1.5px solid #000;
        box-shadow: 1px 1px 3px rgba(0,0,0,0.1);
    }

    /* 1, 3, 5행: 동그라미 */
    .shape-circle { border-radius: 50%; }

    /* 2, 4행: 네모 (모서리를 약간 둥글게) */
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

# 4. 입력창 (필요할 때만 사용)
with st.expander("📝 데이터 수정"):
    edited_df = st.data_editor(st.session_state['inven'], use_container_width=True)
    if st.button("적용"):
        st.session_state['inven'] = edited_df
        st.rerun()

# 5. 겹침 레이아웃 출력
df = st.session_state['inven']
st.markdown('<div class="main-container"><div class="bg-lines"></div>', unsafe_allow_html=True)

for r in range(5):
    is_circle = (r % 2 == 0)
    shape_class = "shape-circle" if is_circle else "shape-square"
    
    # 짝수 행(네모)일 때 좌우로 살짝 밀어서 엇갈리게 배치
    row_style = "margin-left: 65px;" if not is_circle else ""
    
    row_html = f'<div class="row-cont" style="{row_style}">'
    
    sub_df = df.iloc[r*7 : (r+1)*7]
    for _, row in sub_df.iterrows():
        nm = str(row["품목명"])
        lc = str(row["위치코드"])
        try: qt = int(row["수량"])
        except: qt = 0
        
        color_cls = "t-orange" if any(x in nm for x in ["WNS", "WCRS", "WUR"]) else "t-blue"
        bg_cls = "zero-bg" if qt == 0 else ""
        
        row_html += f"""
        <div class="card {shape_class} {bg_cls}">
            <div class="p-n {color_cls}">{nm}</div>
            <div class="p-q">{qt:,}</div>
            <div class="p-l">{lc}</div>
        </div>"""
    
    row_html += '</div>'
    st.markdown(row_html, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
