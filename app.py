import streamlit as st
import pandas as pd

# 1. 페이지 설정
st.set_page_config(page_title="일일 재고 현황표", layout="wide")

# 2. 도면 스타일 CSS (동그라미와 네모/팔각형 디자인 포함)
st.markdown("""
<style>
    .title { text-align: center; font-size: 3.5em; font-weight: bold; text-decoration: underline; margin-bottom: 20px; font-family: 'serif'; }
    
    .main-container {
        position: relative; width: 1080px; margin: 0 auto; padding: 40px 10px;
        background-color: white; border: 1px solid #000; overflow: hidden;
    }

    /* 도면 배경 가로선 */
    .bg-lines {
        position: absolute; top: 0; left: 0; width: 100%; height: 100%; z-index: 1;
        background-image: 
            linear-gradient(to bottom, 
                transparent 105px, #333 105px, #333 106.5px, transparent 106.5px,
                transparent 240px, #333 240px, #333 241.5px, transparent 241.5px,
                transparent 375px, #333 375px, #333 376.5px, transparent 376.5px
            );
    }

    .row-cont { display: flex; justify-content: center; position: relative; z-index: 2; margin-bottom: 5px; }

    /* 공통 카드 스타일 */
    .card {
        width: 130px; height: 130px;
        display: flex; flex-direction: column; justify-content: center; align-items: center;
        background-color: white; margin: 5px; flex-shrink: 0;
        border: 1.5px solid #000; box-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }

    /* 1, 3, 5행: 동그라미 */
    .shape-circle { border-radius: 50%; }

    /* 2, 4행: 네모 (도면 특유의 깎인 네모/팔각형 느낌) */
    .shape-square { border-radius: 15px; border-width: 2px; }

    /* 텍스트 스타일 */
    .p-n { font-weight: bold; font-size: 16px; margin-top: 5px; }
    .p-q { font-size: 20px; font-weight: 900; color: #000; margin: 0; }
    .p-l { color: #8eb44e; font-size: 14px; font-weight: bold; }
    
    .t-blue { color: #0000FF; }
    .t-orange { color: #d35400; }
    .zero-bg { background-color: #fff1f0; }
    .zero-bg .p-q { color: red; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">일 일 재 고 현 황 표</div>', unsafe_allow_html=True)

# 3. 데이터 초기화 (35개 항목)
if 'inven' not in st.session_state:
    st.session_state['inven'] = pd.DataFrame({
        "품목명": ["WASW", "WCRS", "WASW", "WASWP", "WUR", "WNS"] + ["-"] * 29,
        "수량": [1508, 1671, 1754, 1496, 1494, 1686] + [0] * 29,
        "위치코드": ["A101", "A102", "A103", "A104", "A105", "A106"] + [f"A{i}" for i in range(201, 230)]
    })

# 4. 입력 표
with st.expander("📝 데이터 수정"):
    edited_df = st.data_editor(st.session_state['inven'], num_rows="fixed", use_container_width=True)
    if st.button("적용하기"):
        st.session_state['inven'] = edited_df
        st.rerun()

st.divider()

# 5. 도면형 교차 레이아웃 출력
df = st.session_state['inven']
st.markdown('<div class="main-container"><div class="bg-lines"></div>', unsafe_allow_html=True)

for r in range(5):
    # r은 0부터 시작하므로, r % 2 == 0 이면 1, 3, 5행(동그라미) / 아니면 2, 4행(네모)
    is_circle_row = (r % 2 == 0)
    shape_class = "shape-circle" if is_circle_row else "shape-square"
    
    # 2, 4행(네모행)은 도면처럼 약간의 오프셋을 주어 지그재그 느낌 반영
    row_style = "margin-left: 20px;" if not is_circle_row else ""
    
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
