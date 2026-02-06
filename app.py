import streamlit as st
import pandas as pd

# 1. 페이지 설정
st.set_page_config(page_title="일일 재고 현황표", layout="wide")

# 2. CSS: 가로 정렬 강제 및 공백 제거
st.markdown("""
<style>
    .title { text-align: center; font-size: 3em; font-weight: bold; text-decoration: underline; margin-bottom: 20px; }
    
    /* 전체를 감싸는 컨테이너 */
    .main-container {
        display: flex; flex-direction: column; align-items: center; width: 100%;
    }

    /* 행(Row) 설정: 가로로 아이템을 나열 */
    .row-cont { 
        display: flex; 
        justify-content: center; 
        width: 100%; 
        margin-bottom: -50px; /* 위아래 겹침 */
        position: relative;
    }

    /* 네모 행(짝수행) 중앙 정렬을 위한 오프셋 */
    .square-row {
        transform: translateX(65px); /* 동그라미 반 칸만큼 밀어서 사이사이 배치 */
    }

    /* 레이어 순서 */
    .layer-top { z-index: 100; }
    .layer-bottom { z-index: 50; }

    /* 카드 공통 스타일 */
    .card {
        width: 130px; height: 130px;
        display: flex; flex-direction: column; justify-content: center; align-items: center;
        background-color: white; border: 2px solid #000;
        margin: 0 -2px; flex-shrink: 0; /* 가로로 줄어들지 않게 고정 */
        box-shadow: 1px 1px 4px rgba(0,0,0,0.1);
    }

    .shape-circle { border-radius: 50%; }
    .shape-square { border-radius: 15px; }

    /* 텍스트 스타일 */
    .p-n { font-weight: bold; font-size: 14px; margin-bottom: 2px; }
    .p-q { font-size: 19px; font-weight: 900; color: #000; line-height: 1.0; }
    .p-l { color: #8eb44e; font-size: 12px; font-weight: bold; margin-top: 2px; }
    
    .t-blue { color: #0000FF; }
    .t-orange { color: #d35400; }
    .zero-bg { background-color: #fff1f0; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">일 일 재 고 현 황 표</div>', unsafe_allow_html=True)

# 3. 데이터 로드 (세션 상태)
if 'inven' not in st.session_state:
    st.session_state['inven'] = pd.DataFrame({
        "품목명": ["WASW", "WCRS", "WASW", "WASWP", "WUR", "WNS", "WASW"] + ["-"] * 28,
        "수량": [1508, 1671, 1754, 1496, 1494, 1686, 1500] + [0] * 28,
        "위치코드": ["A101", "A102", "A103", "A104", "A105", "A106", "A107"] + [f"A{i}" for i in range(201, 229)]
    })

# 상단 데이터 편집기
with st.expander("📝 데이터 편집기"):
    edited_df = st.data_editor(st.session_state['inven'], use_container_width=True)
    if st.button("수정 내용 저장"):
        st.session_state['inven'] = edited_df
        st.rerun()

# 4. 현황판 출력 (하나의 HTML 문자열로 묶어서 출력해야 세로 배치가 안 됨)
df = st.session_state['inven']
full_html = '<div class="main-container">'

for r in range(5):
    is_circle = (r % 2 == 0)
    layer_cls = "layer-top" if is_circle else "layer-bottom"
    shape_cls = "shape-circle" if is_circle else "shape-square"
    row_type_cls = "" if is_circle else "square-row"
    
    # 각 행의 시작
    full_html += f'<div class="row-cont {layer_cls} {row_type_cls}">'
    
    # 7개씩 끊어서 가로로 배치
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
    full_html += '</div>' # 행 닫기

full_html += '</div>' # 메인 컨테이너 닫기

# 전체 HTML을 단 한 번의 st.markdown으로 출력 (세로 배치 방지 핵심)
st.markdown(full_html, unsafe_allow_html=True)
