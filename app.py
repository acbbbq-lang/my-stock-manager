import streamlit as st
import pandas as pd

st.set_page_config(page_title="일일 재고 현황표", layout="wide")

st.markdown("""
    <style>
    .title { text-align: center; font-size: 3em; font-weight: bold; text-decoration: underline; margin-bottom: 30px; }
    .stock-container { display: flex; flex-wrap: wrap; justify-content: center; background-color: white; padding: 20px; border: 1px solid #ccc; }
    .stock-card {
        border: 1px solid #333; border-radius: 50%; width: 120px; height: 120px;
        display: flex; flex-direction: column; justify-content: center; align-items: center;
        margin: 10px; text-align: center; background-color: white;
    }
    .item-name { font-weight: bold; color: #0000FF; font-size: 0.9em; }
    .item-qty { font-size: 1.2em; font-weight: bold; margin: 2px 0; color: #000; }
    .item-loc { color: #88bb88; font-size: 0.8em; }
    .low-stock { background-color: #ffebee; border-color: #ff0000; }
    .low-stock .item-qty { color: #ff0000; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="title">일 일 재 고 현 황 표</div>', unsafe_allow_html=True)

# 핵심: 세션 데이터를 '완전 빈 데이터프레임'으로 초기화
if 'inventory_data' not in st.session_state:
    st.session_state.inventory_data = pd.DataFrame(columns=["품목명", "수량", "위치코드"])

st.subheader("📝 재고 편집")

# 사용자가 입력한 데이터만 받도록 설정
edited_df = st.data_editor(
    st.session_state.inventory_data,
    num_rows="dynamic",
    use_container_width=True
)

if st.button("수정 내용 적용하기"):
    # 수정한 데이터에서 빈 줄은 빼고 저장
    st.session_state.inventory_data = edited_df.dropna(subset=["품목명"]).copy()
    st.rerun()

st.divider()

df = st.session_state.inventory_data

if not df.empty:
    st.markdown('<div class="stock-container">', unsafe_allow_html=True)
    # 한 줄에 6개 배치를 위한 컬럼 생성
    rows = [df[i:i + 6] for i in range(0, len(df), 6)]
    for row_data in rows:
        cols = st.columns(6)
        for j, (idx, item) in enumerate(row_data.iterrows()):
            # 품목명이 입력된 경우만 카드 생성
            name = str(item["품목명"]).strip() if pd.notnull(item["품목명"]) else ""
            if name:
                with cols[j]:
                    try:
                        qty = float(item["수량"]) if pd.notnull(item["수량"]) else 0.0
                    except:
                        qty = 0.0
                    loc = str(item["위치코드"]) if pd.notnull(item["위치코드"]) else "-"
                    is_low = "low-stock" if qty <= 0 else ""
                    
                    st.markdown(f"""
                        <div class="stock-card {is_low}">
                            <div class="item-name">{name}</div>
                            <div class="item-qty">{int(qty):,}</div>
                            <div class="item-loc">{loc}</div>
                        </div>
                    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


