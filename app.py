import streamlit as st
import pandas as pd

# 1. 화면 설정 (반드시 광폭 레이아웃)
st.set_page_config(page_title="일일 재고 현황표", layout="wide")

# 2. 강력한 가로 배치 CSS
st.markdown("""
<style>
    .title { text-align: center; font-size: 3em; font-weight: bold; text-decoration: underline; margin-bottom: 30px; }
    
    /* 전체 판을 중앙 정렬 */
    .main-board { display: flex; flex-direction: column; align-items: center; width: 100%; overflow-x: auto; }
    
    /* 한 줄에 7개를 가로로 나열하는 핵심 설정 */
    .row-container { 
        display: flex; 
        flex-direction: row; 
        justify-content: center; 
        width: 100%; 
        min-width: 1000px; /* 동그라미들이 줄어들지 않게 최소 너비 고정 */
        margin-bottom: -40px; /* 줄 간격 겹침 효과 */
    }
    
    /* 지그재그를 위한 엇갈림 설정 */
    .zigzag-offset { margin-left: 140px; } 

    .stock-circle {
        border: 2px solid #333; border-radius: 50%; 
        width: 125px; height: 125px;
        display: flex; flex-direction: column; justify-content: center; align-items: center;
        background-color: white; margin: 10px; flex-shrink: 0; /* 크기 유지 */
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    }
    .name { font-weight: bold; color: blue; font-size: 0.85em; margin-bottom: 2px; }
    .qty { font-size: 1.1em; font-weight: bold; color: black; }
    .loc { color: #2e7d32; font-size: 0.75em; font-weight: bold; }
    .zero { background-color: #fff1f0; }
    .zero .qty { color: red; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">일 일 재 고 현 황 표</div>', unsafe_allow_html=True)

# 3. 데이터 초기화 (35개 행)
if 'inven' not in st.session_state:
    st.session_state['inven'] = pd.DataFrame({
        "품목명": [""] * 35, "수량": [0] * 35, "위치코드": [""] * 35
    })

# 4. 입력 표
st.subheader("📝 재고 데이터 입력 (35개 항목)")
edited_df = st.data_editor(st.session_state['inven'], num_rows="fixed", use_container_width=True)

if st.button("수정 내용 적용하기"):
    st.session_state['inven'] = edited_df
    st.rerun()

st.divider()

# 5. 가로 7개씩 5줄 그림 그리기
df = st.session_state['inven']
st.markdown('<div class="main-board">', unsafe_allow_html=True)

for r in range(5): # 5줄 반복
    # 홀수 줄(1, 3번째 줄)은 오른쪽으로 밀어 지그재그 구현
    offset_class = "zigzag-offset" if r % 2 != 0 else ""
    st.markdown(f'<div class="row-container {offset_class}">', unsafe_allow_html=True)
    
    # 해당 줄에 들어갈 7개 품목 데이터
    row_data = df.iloc[r*7 : (r+1)*7]
    
    for _, row in row_data.iterrows():
        p_name = str(row["품목명"]) if row["품목명"] else "-"
        p_loc = str(row["위치코드"]) if row["위치코드"] else ""
        try: q_val = int(row["수량"])
        except: q_val = 0
            
        cls = "zero" if q_val == 0 else ""
        
        # 동그라미 HTML 하나 생성
        circle
