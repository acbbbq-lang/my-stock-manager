import streamlit as st
import pandas as pd

# 1. 페이지 설정 (화면을 넓게 사용)
st.set_page_config(page_title="일일 재고 현황표", layout="wide")

# 2. 이미지와 똑같은 지그재그 스타일 (CSS)
st.markdown("""
<style>
    .title { text-align: center; font-size: 3.5em; font-weight: bold; text-decoration: underline; margin-bottom: 30px; }
    
    /* 전체를 감싸는 컨테이너: 가로로 나열되게 설정 */
    .board-container { 
        display: flex; 
        flex-direction: column; 
        align-items: center; 
        background-color: white; 
        width: 100%;
    }

    /* 한 줄을 담당하는 상자: 안의 내용물을 가로(row)로 배치 */
    .stock-row { 
        display: flex; 
        flex-direction: row; 
        justify-content: center; 
        width: 100%; 
        margin-bottom: -40px; /* 줄 사이 간격을 좁혀서 겹치게 함 */
    }

    /* 지그재그를 위해 홀수 줄을 오른쪽으로 살짝 밀기 */
    .row-offset { padding-left: 140px; }

    .stock-card {
        border: 1.5px solid #333; border-radius: 50%; width: 130px; height: 130px;
        display: flex; flex-direction: column; justify-content: center; align-items: center;
        background-color: white; margin: 10px; z-index: 2;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    }

    .item-name { font-weight: bold; color: #0000FF; font-size: 1em; }
    .item-qty { font-size: 1.3em; font-weight: bold; color: #000; margin: 2px 0; }
    .item-loc { color: #8DB48E; font-size: 0.9em; font-weight: bold; }
    
    /* 수량 0일 때 스타일 */
    .out-of-stock { background-color: #FDF2F4; }
    .out-of-stock .item-qty { color: #FF0000; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">일 일 재 고 현 황 표</div>', unsafe_allow_html=True)

# 3. 데이터 초기화
if 'inventory_data' not in st.session_state:
    st.session_state.inventory_data = pd.DataFrame(columns=["품목명", "수량", "위치코드"])

st.subheader("📝 재고 데이터 입력")
edited_df = st.data_editor(
    st.session_state.inventory_data, 
    num_rows="dynamic", 
    use_container_width=True, 
    hide_index=True
)

# 4. 수정 내용 적용 (비어있는 행 제거 로직)
if st.button("수정 내용 적용하기"):
    if edited_df is not None:
        # 품목명이 비어있거나 'None'인 행을 완전히 제거 (1행 필요없음 해결)
        df_new = edited_df.dropna(subset=["품목명"]).copy()
        df_new = df_new[df_new["품목명"].astype(str).str.strip() != ""]
        st.session_state.inventory_data = df_new.reset_index(drop=True)
        st.rerun()

st.divider()

# 5. 지그재그 현황판 출력
df = st.session_state.inventory_data
if not df.empty:
    st.markdown('<div class="board-container">', unsafe_allow_html=True)
    
    # 6개씩 끊어서 가로 줄 생성
    for i in range(0, len(df), 6):
        # 홀수 줄(두 번째 줄 등)에만 row-offset 클래스 추가
        is_offset = "row-offset" if (i // 6) % 2 != 0 else ""
        st.markdown(f'<div class="stock-row {is_offset}">', unsafe_allow_html=True)
        
        row_data = df.iloc[i : i+6]
        for _, item in row_data.iterrows():
            name = str(item.get("품목명", "")).strip()
            loc = str(item.get("위치코드", "")).strip() if pd.notnull(item.get("위치코드")) else ""
            try:
                qty = int(float(item.get("수량", 0)))
            except:
                qty = 0
            
            bg = "out-of-stock" if qty == 0 else ""
            
            card = f'<div class="stock-card {bg}">'
            card += f'<div class="item-name">{name}</div>'
            card += f'<div class="item-qty">{qty:,}</div>'
            card += f'<div class="item-loc">{loc}</div></div>'
            st.markdown(card, unsafe_allow_html=True)
            
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.info("데이터를 입력하고 '수정 내용 적용하기' 버튼을 눌러주세요.")
