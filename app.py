import streamlit as st
import pandas as pd

# 1. 페이지 설정
st.set_page_config(page_title="일일 재고 현황표", layout="wide")

# 2. CSS 설정: 동그라미(z-index:10)가 네모(z-index:5) 위로 오게 고정
st.markdown("""
<style>
    .title { text-align: center; font-size: 3.5em; font-weight: bold; text-decoration: underline; margin-bottom: 20px; }
    
    .main-container {
        position: relative; width: 1050px; margin: 0 auto; padding: 20px 0px;
        background-color: white; min-height: 600px;
    }

    /* 도면 뒷 배경 가로선 */
    .bg-lines {
        position: absolute; top: 0; left: 0; width: 100%; height: 100%; z-index: 1;
        background-image: 
            linear-gradient(to bottom, 
                transparent 80px, #000 80px, #000 81.5px, transparent 81.5px,
                transparent 200px, #000 200px, #000 201.5px, transparent 201.5px,
                transparent 320px, #000 320px, #000 321.5px, transparent 321.5px
            );
    }

    /* 행 간격: 음수 마진으로 위아래 겹침 구현 */
    .row-cont { 
        display: flex; justify-content: center; position: relative; 
        margin-bottom: -55px; /* 이 수치로 위아래 겹침 조절 */
    }

    /* 카드 공통 스타일 */
    .card {
        width: 135px; height: 135px;
        display: flex; flex-direction: column; justify-content: center; align-items: center;
        background-color: white; margin: 0 -10px; flex-shrink: 0;
        border: 2px solid #000; box-shadow: 2px 2px 5px rgba(0,0,0,0.2);
    }

    /* 1, 3, 5행: 동그라미 (z-index를 높게!) */
    .row-up { z-index: 20 !important; }
    .shape-circle { border-radius: 50%; }

    /* 2, 4행: 네모 (z-index를 낮게!) */
    .row-down { z-index: 10 !important; }
    .shape-square { border-radius: 12px; }

    /* 텍스트 스타일 */
    .p-n { font-weight: bold; font-size: 15px; }
    .p-q { font-size: 20px; font-weight: 900; color: #000; margin: 2px 0; }
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

# 4. 입력창 (필요할 때만 펼치기)
with st.expander("📝 데이터 수정하기"):
    edited_df = st.data_editor(st.session_state['inven'], use_container_width=True)
    if st.button("수정 내용 저장"):
        st.session_state['inven'] = edited_df
        st.rerun()

# 5. 현황판 출력부
df = st.session_state['inven']
# 컨테이너 시작
st.markdown('<div class="main-container"><div class="bg-lines"></div>', unsafe_allow_html=True)

for r in range(5):
    is_circle_row = (r % 2 == 0)
    # 레이어 높낮이(z-index)와 모양 클래스 지정
    row_lv = "row-up" if is_circle_row else "row-down"
    shape_cls = "shape-circle" if is_circle_row else "shape-square"
    
    # 지그재그 정렬: 네모 행은 오른쪽으로 이동
    row_style = "margin-left: 70px;" if not is_circle_row else ""
    
    row_html = f'<div class="row-cont {row_lv}" style="{row_style}">'
    
    sub_df = df.iloc[r*7 : (r+1)*7]
    for _, row in sub_df.iterrows():
        nm, lc, qt = str(row["품목명"]), str(row["위치코드"]), int(row["수량"])
