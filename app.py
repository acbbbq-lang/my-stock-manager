import streamlit as st
import pandas as pd

# 1. 페이지 설정
st.set_page_config(page_title="일일 재고 현황표", layout="wide")

# 2. CSS: 가로 정렬 고정 및 도면 스타일 재현
st.markdown("""
<style>
    .title { text-align: center; font-size: 3.5em; font-weight: bold; text-decoration: underline; margin-bottom: 20px; }
    
    /* 전체를 감싸는 컨테이너 */
    .main-container {
        display: flex; flex-direction: column; align-items: center; width: 100%; min-width: 1000px;
    }

    /* 행(Row): 요소들을 가로로 나열 */
    .row-cont { 
        display: flex; justify-content: center; width: 100%; 
        margin-bottom: -55px; /* 위아래 도형이 맞물리도록 설정 */
    }

    /* 네모 행(짝수행): 동그라미 사이사이로 들어가도록 절반 칸 이동 */
    .square-row { transform: translateX(65px); }

    /* 레이어 순서: 동그라미가 네모 위로 */
    .layer-top { z-index: 100; }
    .layer-bottom { z-index: 50; }

    /* 카드 공통 스타일 */
    .card {
        width: 130px; height: 130px;
        display: flex; flex-direction: column; justify-content: center; align-items: center;
        background-color: white; border: 2.5px solid #000;
        margin: 0 -3px; flex-shrink: 0; /* 가로 크기 유지 */
        box-shadow: 1px 1px 4px rgba(0,0,0,0.15);
    }

    .shape-circle { border-radius: 50%; }
    .shape-square { border-radius: 15px; }

    /* 텍스트 스타일 */
    .p-n { font-weight: bold; font-size: 14px; margin-bottom: 2px; }
    .p-q { font-size: 20px; font-weight: 900; color: #000; line-height: 1.0; }
    .p-l { color: #8eb44e; font-size: 12px; font-weight: bold; margin-top: 2px; }
    
    .t-blue { color: #0000FF; }
    .t-orange { color: #d35400; }
    .zero-bg { background-color: #fff1f0; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">일 일 재 고 현 황 표</div>', unsafe_allow_html=True)

# 3. 데이터 로드 (세션 상태)
if 'inven' not in st.session_state:
    # 엑셀 도면 기준 샘플 데이터
    st.session_state['inven'] = pd.DataFrame({
        "품목명": ["WASW", "WCRS", "WASW", "WASWP", "WUR", "WNS", "WASW"] + ["-"] * 28,
        "수량": [1508, 1671, 1754, 1496, 1494, 1686, 1500] + [0] * 28,
        "위치코드": ["A101", "A102", "A103", "A104", "A105", "A106", "A107"] + [f"A{i}" for i in range(201, 229)]
    })

# 상단 데이터 편집기
with st.expander("📝 재고 수량 수정하기"):
    edited_df = st.data_editor(st.session_state['inven'], use_container_width=True)
    if st.button("내용 저장 및 반영"):
        st.session_state['inven'] = edited_df
        st.rerun()

# 4. 현황판 생성 (모든 HTML을 하나의 변수에 담아 한 번에 출력)
df = st.session_state['inven']
full_html = '<div class="main-container">'

for r in range(5):
    is_circle = (r % 2 == 0)
    layer_cls = "layer-top" if is_circle else "layer-bottom"
    shape_cls = "shape-circle" if is_circle else "shape-square"
    row_type_cls = "" if is_circle else "square-row"
    
    # 행 시작
    full_html += f'<div class="row-cont {layer_cls} {row_type_cls}">'
    
    # 해당 행의 데이터 가져오기 (행당 7개)
    sub_df = df.iloc[r*7 : (r+1)*7]
    for _, row in sub_df.iterrows():
        nm, lc, qt = str(row["품목명"]), str(row["위치코드"]), int(row["수량"])
        c_cls = "t-orange" if any(x in nm for x in ["WNS", "WCRS", "WUR"]) else "t-blue"
        bg_cls = "zero-bg" if qt == 0 else ""
        
        full_html += f"""
        <div class="card {shape_cls} {bg_cls}">
            <div class="p-n {c_cls}">{nm}</div>
            <div class="p-q">{qt:,}</div>
            <div class="p-l">{lc}</div>
        </div>
        """
    full_html += '
