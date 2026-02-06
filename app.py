import streamlit as st
import pandas as pd

# 1. 페이지 설정
st.set_page_config(page_title="일일 재고 현황표", layout="wide")

# 2. CSS 수정 (맨 위 테두리 제거 및 도면 스타일 최적화)
st.markdown("""
<style>
    /* 제목 스타일 */
    .title { text-align: center; font-size: 3.5em; font-weight: bold; text-decoration: underline; margin-bottom: 30px; font-family: 'serif'; }
    
    /* 전체 컨테이너: 테두리 제거(border: none) */
    .main-container {
        position: relative; width: 1100px; margin: 0 auto; padding: 20px 0px;
        background-color: white; border: none; overflow: hidden;
    }

    /* 도면 가로선 배경 (7개씩 5줄 높이에 맞춰 조정) */
    .bg-lines {
        position: absolute; top: 0; left: 0; width: 100%; height: 100%; z-index: 1;
        background-image: 
            linear-gradient(to bottom, 
                transparent 75px, #000 75px, #000 76.5px, transparent 76.5px,
                transparent 215px, #000 215px, #000 216.5px, transparent 216.5px,
                transparent 355px, #000 355px, #000 356.5px, transparent 356.5px,
                transparent 495px, #000 495px, #000 496.5px, transparent 496.5px
            );
    }

    .row-cont { display: flex; justify-content: center; position: relative; z-index: 2; margin-bottom: 10px; }

    /* 카드 공통 스타일 */
    .card {
        width: 130px; height: 130px;
        display: flex; flex-direction: column; justify-content: center; align-items: center;
        background-color: white; margin: 4px; flex-shrink: 0;
        border: 1.5px solid #000; box-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }

    /* 1, 3, 5행: 동그라미 */
    .shape-circle { border-radius: 50%; }

    /* 2, 4행: 네모 (모서리가 둥근 사각형) */
    .shape-square { border-radius: 15px; }

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
        "품목명": ["WASW", "WCRS", "WASW", "WASWP", "WUR", "WNS", "11"] + ["-"] * 28,
        "수량": [1508, 1671, 1754, 1496, 1494, 1686, 11] + [0] * 28,
        "위치코드": ["A101", "A102", "A103", "A104", "A105", "A106", "A201"] + [f"A{i}" for i in range(202, 230)]
    })

# 4. 입력 표 (수정 시에만 열기)
with st.expander("📝 데이터 입력창 열기"):
    edited_df = st.data_editor(st.session_state['inven'], num_rows="fixed", use_container_width=True)
    if st.button("수정 내용 적용"):
        st.session_state['inven'] = edited_df
        st.rerun()

st.divider()

# 5. 현황판 출력
df = st.session_state['inven']
# 테두리 없는 컨테이너 시작
st.markdown('<div class="main-container"><div class="bg-lines"></div>', unsafe_allow_html=True)

for r in range(5):
    # 행에 따라 모양 결정 (0,2,4행은 동그라미 / 1,3행은 네모)
    is_circle_row = (r % 2 == 0)
    shape_class = "shape-circle" if is_circle_row else "shape-square"
    
    row_html = f'<div class="row-cont">'
    
    sub_df = df.iloc[r*7 : (r+1)*7]
    for _, row in sub_df.iterrows():
        nm = str(row["품목명"])
        lc = str(row["위치코드"])
        try: qt = int(row["수량"])
        except: qt = 0
        
        # 글자 색상 자동 설정
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
