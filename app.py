import streamlit as st
import pandas as pd

# 1. 페이지 설정
st.set_page_config(page_title="일일 재고 현황표", layout="wide")

# 2. 카드 디자인 스타일
st.markdown("""
<style>
    .title { text-align: center; font-size: 3em; font-weight: bold; text-decoration: underline; margin-bottom: 30px; }
    .stock-container { display: flex; flex-wrap: wrap; justify-content: center; background-color: white; padding: 20px; border: 1px solid #ccc; min-height: 200px; }
    .stock-card {
        border: 1px solid #333; border-radius: 50%; width: 130px; height: 130px;
        display: flex; flex-direction: column; justify-content: center; align-items: center;
        margin: 15px; text-align: center; background-color: white;
    }
    .item-name { font-weight: bold; color: #0000FF; font-size: 0.9em; margin-bottom: 5px; }
    .item-qty { font-size: 1.3em; font-weight: bold; color: #000; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">일 일 재 고 현 황 표</div>', unsafe_allow_html=True)

# 3. 데이터 저장소 관리
if 'inventory_data' not in st.session_state:
    st.session_state.inventory_data = pd.DataFrame(columns=["품목명", "수량"])

st.subheader("📝 재고 편집")

# 4. 재고 입력 표 (0번 행부터 바로 입력 가능)
edited_df = st.data_editor(
    st.session_state.inventory_data,
    num_rows="dynamic",
    use_container_width=True,
    hide_index=True
)

# 5. 적용 버튼 (클릭 시 화면 갱신)
if st.button("수정 내용 적용하기"):
    if edited_df is not None:
        # 품목명이 입력된 행만 필터링하여 저장
        df_clean = edited_df.dropna(subset=["품목명"])
        df_clean = df_clean[df_clean["품목명"].astype(str).str.strip() != ""]
        st.session_state.inventory_data = df_clean.reset_index(drop=True)
        st.rerun()

st.divider()

# 6. 동그란 현황판 출력 로직
df = st.session_state.inventory_data

if not df.empty:
    # 카드들을 담는 큰 그릇 시작
    st.markdown('<div class="stock-container">', unsafe_allow_html=True)
    
    for _, item in df.iterrows():
        name = str(item["품목명"]).strip()
        try:
            # 수량에서 소수점이나 쉼표 제거 후 정수로 변환
            val = float(item["수량"]) if pd.notnull(item["수량"]) else 0
            qty = int(val)
        except:
            qty = 0
            
        # 개별 동그라미 카드 HTML 생성
        card_html = f"""
        <div class="stock-card">
            <div class="item-
