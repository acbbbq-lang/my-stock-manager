import streamlit as st
import pandas as pd

# 1. 페이지 설정 (가로로 넓게 사용)
st.set_page_config(page_title="일일 재고 현황표", layout="wide")

# 2. CSS 디자인 (가로 정렬 및 지그재그 효과 강제 적용)
st.markdown("""
<style>
    .title { text-align: center; font-size: 3.5em; font-weight: bold; text-decoration: underline; margin-bottom: 40px; }
    .board-container { display: flex; flex-direction: column; align-items: center; width: 100%; padding: 20px; }
    
    /* 핵심: 세로 배치를 가로 배치로 변경 */
    .stock-row { 
        display: flex; 
        flex-direction: row; 
        justify-content: center; 
        width: 100%; 
        margin-bottom: -45px; 
    }
    .row-offset { margin-left: 140px; } /* 지그재그 효과 */
    
    .stock-card {
        border: 1.5px solid #333; border-radius: 50%; width: 130px; height: 130px;
        display: flex; flex-direction: column; justify-content: center; align-items: center;
        background-color: white; margin: 10px; z-index: 2;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    }
    .item-name { font-weight: bold; color: #0000FF; font-size: 0.95em; }
    .item-qty { font-size: 1.3em; font-weight: bold; color: #000; margin: 3px 0; }
    .item-loc { color: #8DB48E; font-size: 0.85em; font-weight: bold; }
    
    /* 수량 0일 때 스타일 */
    .out-of-stock { background-color: #FDF2F4; }
    .out-of-stock .item-qty { color: #FF0000; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">일 일 재 고 현 황 표</div>', unsafe_allow_html=True)

# 3. 데이터 초기화
if 'inventory_data' not in st.session_state:
    st.session_state['inventory_data'] = pd.DataFrame(columns=["품목명", "수량", "위치코드"])

# 4. 데이터 입력 표 (이 부분이 항상 보여야 합니다)
st.subheader("📝 재고 데이터 입력")
edited_df = st.data_editor(
    st.session_state['inventory_data'],
    num_rows="dynamic",
    use_container_width=True,
    hide_index=True,
    key="inventory_editor"
)

# [수정 내용 적용하기] 버튼
if st.button("수정 내용 적용하기"):
    if edited_df is not None:
        # 품목명이 있는 행만 필터링해서 저장
        df_clean = edited_df.dropna(subset=["품목명"]).copy()
        df_clean = df_clean[df_clean["품목명"].astype(str).str.strip() != ""]
        st.session_state['inventory_data'] = df_clean.reset_index(drop=True)
        st.rerun()

st.divider()

# 5. 가로 지그재그 현황판 출력 로직
df = st.session_state['inventory_data']

if not df.empty:
    st.markdown('<div class="board-container">', unsafe_allow_html=True)
    
    # 6개씩 끊어서 가로 한 줄(Row)씩 생성
    for i in range(0, len(df), 6):
        row_num = i // 6
        # 홀수 줄(1, 3, 5...)은 row-offset 클래스를 추가하여 옆으로 밀기
        offset_class = "row-offset" if row_num % 2 != 0 else ""
        
        # 가로 줄 시작
        st.markdown(f'<div class="stock-row {offset_class}">', unsafe_allow_html=True)
        
        row_items = df.iloc[i : i + 6]
        for _, item in row_items.iterrows():
            name = str(item.get("품목명", "")).strip()
            loc = str(item.get("위치코드", "")) if pd.notnull(item.get("위치코드")) and str(item.get("위치코드")) != "None" else ""
            
            # 수량 처리: 데이터가 없거나 비어있으면 0으로 표시
            try:
                val = item.get("수량")
                qty = int(float(val)) if pd.notnull(val) and str(val).strip() != "" else 0
            except:
                qty = 0
            
            # 수량 0이면 빨간색 배경 적용
            bg_class = "out-of-stock" if qty == 0 else ""
            
            card_html = f"""
            <div class="stock-card {bg_class}">
                <div class="item-name">{name}</div>
                <div class="item-qty">{qty:,}</div>
                <div class="item-loc">{loc}</div>
            </div>
            """
            st.markdown(card_html, unsafe_allow_html=True)
            
        # 가로 줄 종료
        st.markdown('</div>', unsafe_allow_html=True)
        
    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.info("💡 위 표에 재고 정보를 입력한 후 [수정 내용 적용하기] 버튼을 눌러주세요.")
