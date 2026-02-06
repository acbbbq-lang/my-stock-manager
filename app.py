import streamlit as st
import pandas as pd

# 1. 페이지 설정
st.set_page_config(page_title="일일 재고 현황표", layout="wide")

# 2. CSS: 그리드 시스템을 이용한 완벽한 중앙 정렬 및 겹침
st.markdown("""
<style>
    .title { text-align: center; font-size: 3.5em; font-weight: bold; text-decoration: underline; margin-bottom: 20px; }
    
    /* 전체 컨테이너: 모든 요소를 중앙으로 */
    .main-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        width: 100%;
        padding: 0;
    }

    /* 행 레이아웃: 그리드를 사용하여 칸을 딱 맞춤 */
    .row-cont { 
        display: grid;
        grid-template-columns: repeat(7, 130px); /* 7개 열 고정 */
        gap: 0px; /* 좌우 간격 제거 */
        justify-content: center; /* 그리드 전체를 중앙으로 */
        position: relative;
        margin-bottom: -50px; /* 위아래 도형 겹침 (공백 제거) */
    }

    /* 네모 행(2, 4행) 전용: 반 칸(65px)만큼 왼쪽/오른쪽 여백을 주어 지그재그 중앙 정렬 */
    .square-row {
        padding-left: 130px; /* 시작 위치를 반 칸 옆으로 밀어서 중앙 밸런스 유지 */
        grid-template-columns: repeat(6, 130px); /* 네모는 보통 사이사이에 들어가므로 개수 조절 가능 */
    }

    /* 레이어 순서 */
    .layer-top { z-index: 100 !important; }
    .layer-bottom { z-index: 50 !important; }

    /* 카드 스타일 */
    .card {
        width: 130px; height: 130px;
        display: flex; flex-direction: column; justify-content: center; align-items: center;
        background-color: white; 
        border: 2px solid #000;
        box-shadow: 1px 1px 4px rgba(0,0,0,0.1);
        margin: 0 -2px; /* 아주 미세한 겹침으로 빈틈 제거 */
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
    if st.button("저장"):
        st.session_state['inven'] = edited_df
        st.rerun()

# 4. 현황판 출력
df = st.session_state['inven']
st.markdown('<div class="main-container">', unsafe_allow_html=True)

for r in range(5):
    is_circle = (r % 2 == 0)
    layer_cls = "layer-top" if is_circle else "layer-bottom"
    shape_cls = "shape-circle" if is_circle else "shape-square"
    row_type_cls = "" if is_circle else "square-row" # 네모 행일 때만 중앙 정렬용 클래스 추가
    
    # 행 시작
    st.markdown(f'<div class="row-cont {layer_cls} {row_type_cls}">', unsafe_allow_html=True)
    
    # 지그재그 정렬을 위해 네모 행은 6개만 배치하거나 범위를 조절
    display_count = 7 if is_circle else 6
    sub_df = df.iloc[r*7 : r*7 + display_count]
    
    for _, row in sub_df.iterrows():
        nm, lc, qt = str(row["품목명"]), str(row["위치코드"]), int(row["수량"])
        c_cls = "t-orange" if any(x in nm for x in ["WNS", "WCRS", "WUR"]) else "t-blue"
        bg_cls = "zero-bg" if qt == 0 else ""
        
        card_html = f"""
        <div class="card {shape_cls} {bg_cls}">
            <div class="p-n {c_cls}">{nm}</div>
            <div class="p-q">{qt:,}</div>
            <div class="p-l">{lc}</div>
        </div>
        """
        st.markdown(card_html, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
