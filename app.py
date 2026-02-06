import streamlit as st
import pandas as pd

# 1. 페이지 설정
st.set_page_config(page_title="일일 재고 현황표", layout="wide")

# 2. CSS 설정: 동그라미(z-index: 100) > 네모(z-index: 50) > 배경선(z-index: 1)
st.markdown("""
<style>
    .title { text-align: center; font-size: 3.5em; font-weight: bold; text-decoration: underline; margin-bottom: 30px; }
    
    .main-container {
        position: relative; 
        width: 1050px; 
        margin: 0 auto; 
        padding: 40px 0;
        background-color: white;
        min-height: 800px; /* 컨테이너가 쪼그라들지 않도록 최소 높이 설정 */
    }

    /* 도면 뒷 배경 가로선 - 가장 뒤에 배치 (z-index: 1) */
    .bg-lines {
        position: absolute; top: 0; left: 0; width: 100%; height: 100%; z-index: 1;
        background-image: 
            linear-gradient(to bottom, 
                transparent 100px, #000 100px, #000 101.5px, transparent 101.5px,
                transparent 240px, #000 240px, #000 241.5px, transparent 241.5px,
                transparent 380px, #000 380px, #000 381.5px, transparent 381.5px,
                transparent 520px, #000 520px, #000 521.5px, transparent 521.5px
            );
    }

    /* 행 레이아웃: 위아래가 겹치도록 마진 설정 */
    .row-cont { 
        display: flex; 
        justify-content: center; 
        position: relative; 
        margin-bottom: -60px; /* 위아래 카드가 겹치는 정도 */
    }

    /* 동그라미 행 (1, 3, 5행) - z-index 최상단 */
    .up-layer { z-index: 100 !important; }
    /* 네모 행 (2, 4행) - z-index 중간 */
    .down-layer { z-index: 50 !important; }

    /* 카드 공통 스타일 */
    .card {
        width: 135px; height: 135px;
        display: flex; flex-direction: column; justify-content: center; align-items: center;
        background-color: white; 
        margin: 0 -12px; /* 좌우 카드가 겹치는 정도 */
        flex-shrink: 0;
        border: 2px solid #000;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.15);
    }

    .shape-circle { border-radius: 50%; }
    .shape-square { border-radius: 12px; }

    /* 텍스트 스타일 */
    .p-n { font-weight: bold; font-size: 15px; }
    .p-q { font-size: 22px; font-weight: 900; color: #000; margin: 2px 0; }
    .p-l { color: #8eb44e; font-size: 14px; font-weight: bold; }
    
    .t-blue { color: #0000FF; }
    .t-orange { color: #d35400; }
    .zero-bg { background-color: #fff1f0; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">일 일 재 고 현 황 표</div>', unsafe_allow_html=True)

# 3. 데이터 로드 (세션 상태 유지)
if 'inven' not in st.session_state:
    st.session_state['inven'] = pd.DataFrame({
        "품목명": ["WASW", "WCRS", "WASW", "WASWP", "WUR", "WNS", "WASW"] + ["-"] * 28,
        "수량": [1508, 1671, 1754, 1496, 1494, 1686, 1500] + [0] * 28,
        "위치코드": ["A101", "A102", "A103", "A104", "A105", "A106", "A107"] + [f"A{i}" for i in range(201, 229)]
    })

# 4. 데이터 수정 인터페이스
with st.expander("📝 데이터 편집기 열기"):
    edited_df = st.data_editor(st.session_state['inven'], use_container_width=True)
    if st.button("수정 완료"):
        st.session_state['inven'] = edited_df
        st.rerun()

# 5. 현황판 출력
df = st.session_state['inven']
# 전체 컨테이너 시작
st.markdown('<div class="main-container">', unsafe_allow_html=True)
# 배경선 먼저 깔기
st.markdown('<div class="bg-lines"></div>', unsafe_allow_html=True)

for r in range(5):
    is_circle_row = (r % 2 == 0)
    
    # 층(Layer) 결정: 동그라미 행은 up-layer, 네모 행은 down-layer
    layer_cls = "up-layer" if is_circle_row else "down-layer"
    shape_cls = "shape-circle" if is_circle_row else "shape-square"
    
    # 지그재그 정렬: 네모 행은 약간 우측으로
    row_style = "margin-left: 75px;" if not is_circle_row else ""
    
    # 행 시작
    st.markdown(f'<div class="row-cont {layer_cls}" style="{row_style}">', unsafe_allow_html=True)
    
    sub_df = df.iloc[r*7 : (r+1)*7]
    for _, row in sub_df.iterrows():
        nm = str(row["품목명"])
        lc = str(row["위치코드"])
        qt = int(row["수량"])
        
        c_cls = "t-orange" if any(x in nm for x in ["WNS", "WCRS", "WUR"]) else "t-blue"
        bg = "zero-bg" if qt == 0 else ""
        
        card_html = f"""
        <div class="card {shape_cls} {bg}">
            <div class="p-n {c_cls}">{nm}</div>
            <div class="p-q">{qt:,}</div>
            <div class="p-l">{lc}</div>
        </div>
        """
        st.markdown(card_html, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True) # 행 닫기

st.markdown('</div>', unsafe_allow_html=True) # 컨테이너 닫기
