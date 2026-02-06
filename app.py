import streamlit as st
import pandas as pd

# 1. 화면 전체 너비 사용 설정
st.set_page_config(page_title="일일 재고 현황표", layout="wide")

# 2. 가로 정렬을 위한 특수 디자인 (CSS)
st.markdown("""
<style>
    .title { text-align: center; font-size: 3.5em; font-weight: bold; text-decoration: underline; margin-bottom: 40px; }
    
    /* 카드들을 가로로 나열하는 컨테이너 */
    .stock-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(150px, 1fr)); /* 자동으로 가로 꽉 채우기 */
        gap: 20px;
        padding: 20px;
        justify-items: center;
    }

    .stock-card {
        border: 1px solid #333;
        border-radius: 50%;
        width: 140px;
        height: 140px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        background-color: white;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    }
    .item-name { font-weight: bold; color: #0000FF; font-size: 0.9em; margin-bottom: 5px; }
    .item-qty { font-size: 1.4em; font-weight: bold; color: #000; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">일 일 재 고 현 황 표</div>', unsafe_allow_html=True)

# 3. 데이터 관리
if 'inventory_data' not in st.session_state:
    st.session_state.inventory_data = pd.DataFrame(columns=["품목명", "수량"])

st.subheader("📝 재고 편집")
edited_df = st.data_editor(
    st.session_state.inventory_data,
    num_rows="dynamic",
    use_container_width=True,
    hide_index=True
)

if st.button("수정 내용 적용하기"):
    if edited_df is not None:
        df_clean = edited_df.dropna(subset=["품목명"]).copy()
        df_clean = df_clean[df_clean["품목명"].astype(str).str.strip() != ""]
        st.session_state.inventory_data = df_clean.reset_index(drop=True)
        st.rerun()

st.divider()

# 4. 현황판 출력 (가로 그리드 적용)
df = st.session_state.inventory_data

if not df.empty:
    # 그리드 시작
    st.markdown('<div class="stock-grid">', unsafe_allow_html=True)
    
    for _, item in df.iterrows():
        name = str(item["품목명"]).strip()
        try:
            qty_val = int(float(item["수량"])) if pd.notnull(item["수량"]) else 0
        except:
            qty_val = 0
            
        # 개별 카드 생성
        card_html = f"""
        <div class="stock-card">
            <div class="item-name">{name}</div>
            <div class="item-qty">{qty_val:,}</div>
        </div>
        """
        st.markdown(card_html, unsafe_allow_html=True)
        
    # 그리드 끝
    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.info("데이터가 없습니다. 위 표에 내용을 입력하고 버튼을 눌러주세요.")
