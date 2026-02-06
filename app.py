import streamlit as st
import pandas as pd
from io import StringIO

# 1. 페이지 설정
st.set_page_config(page_title="일일 재고 현황표", layout="wide")

# 2. CSS: 네모 확대 및 위아래 완전 밀착
st.markdown("""
<style>
    .title { text-align: center; font-size: 3em; font-weight: bold; text-decoration: underline; margin-bottom: 20px; }
    
    .main-container {
        display: flex; flex-direction: column; align-items: center; width: 100%;
    }

    .row-cont { 
        display: flex; 
        justify-content: center; 
        width: 100%; 
        /* 네모가 커져서 겹침 강도를 -85px로 설정하여 빈틈 제거 */
        margin-bottom: -85px; 
        position: relative;
    }

    .row-cont:last-child { margin-bottom: 100px; }

    .layer-top { z-index: 100; }
    .layer-bottom { z-index: 50; }

    .card {
        display: flex; flex-direction: column; justify-content: center; align-items: center;
        background-color: white; border: 2.5px solid #000;
        margin: 0 -8px; flex-shrink: 0;
        box-shadow: 2px 2px 6px rgba(0,0,0,0.1);
    }

    /* 동그라미 크기 유지 */
    .shape-circle { width: 130px; height: 130px; border-radius: 50%; }

    /* 네모 크기 대폭 확대 */
    .shape-square { 
        width: 190px; height: 170px; 
        border-radius: 10px; 
        background-color: #fcfcfc;
    }

    /* 텍스트 시인성 확보 */
    .p-n { font-weight: bold; font-size: 16px; margin-bottom: 4px; }
    .p-q { font-size: 26px; font-weight: 900; color: #000; line-height: 1.0; }
    .p-l { color: #8eb44e; font-size: 14px; font-weight: bold; margin-top: 4px; }
    
    .t-blue { color: #0000FF; }
    .t-orange { color: #d35400; }
    .zero-bg { background-color: #fff1f0; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">일 일 재 고 현 황 표</div>', unsafe_allow_html=True)

# 3. 데이터 로직 (세션 상태 유지)
if 'inven' not in st.session_state:
    st.session_state['inven'] = pd.DataFrame({
        "품목명": ["-"] * 35,
        "수량": [0] * 35,
        "위치코드": ["-"] * 35
    })

# --- 엑셀 복사 붙여넣기 칸 ---
with st.expander("📋 엑셀 데이터 복사해서 붙여넣기"):
    st.info("엑셀에서 3개 열(품목명, 수량, 위치코드)을 복사(Ctrl+C)한 뒤 아래에 붙여넣으세요.")
    input_text = st.text_area("여기에 붙여넣기 (Ctrl+V)", height=150)
    
    if st.button("붙여넣은 내용 반영하기"):
        if input_text:
            try:
                # 엑셀 복사 시 탭(tab)으로 구분됨
                new_df = pd.read_csv(StringIO(input_text), sep='\t', names=["품목명", "수량", "위치코드"])
                
                # 데이터가 부족하면 빈 행으로 채움
                if len(new_df) < 35:
                    extra = pd.DataFrame([["-", 0, "-"]] * (35 - len(new_df)), columns=["품목명", "수량", "위치코드"])
                    new_df = pd.concat([new_df, extra], ignore_index=True)
                
                st.session_state['inven'] = new_df.head(35)
                st.success("데이터가 성공적으로 업데이트되었습니다!")
                st.rerun()
            except Exception as e:
                st.error(f"오류가 발생했습니다: {e}")

# 4. 현황판 출력 (SyntaxError 방지를 위한 안전한 문자열 생성)
df = st.session_state['inven']
full_html = '<div class="main-container">'

current_idx = 0
for r in range(5):
    is_circle = (r % 2 == 0)
    layer_cls = "layer-top" if is_circle else "layer-bottom"
    shape_cls = "shape-circle" if is_circle else "shape-square"
    count = 6 if is_circle else 7
    
    full_html += f'<div class="row-cont {layer_cls}">'
    
    sub_df = df.iloc[current_idx : current_idx + count]
    for _, row in sub_df.iterrows():
        nm, lc, qt = str(row["품목명"]), str(row["위치코드"]), int(row["수량"])
        c_cls = "t-orange" if any(x in nm for x in ["WNS", "WCRS", "WUR"]) else "t-blue"
        bg_cls = "zero-bg" if qt == 0 else ""
        
        # HTML 내부 줄바꿈 없이 한 줄로 작성 (에러 방지)
        card_html = f'<div class="card {shape_cls} {bg_cls}"><div class="p-n {c_cls}">{nm}</div><div class="p-q">{qt:,}</div><div class="
