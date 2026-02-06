import streamlit as st
import pandas as pd

# 1. 페이지 설정
st.set_page_config(page_title="일일 재고 현황표", layout="wide")

# 2. 도면 스타일 CSS (격자 배경 선 + 지그재그 배치)
st.markdown("""
<style>
    .title { text-align: center; font-size: 3.5em; font-weight: bold; text-decoration: underline; margin-bottom: 20px; font-family: 'Times New Roman', serif; }
    
    /* 도면 전체 판 */
    .main-container {
        position: relative; width: 1050px; margin: 0 auto; padding: 60px 20px;
        background-color: white; border: 1px solid #000; overflow: hidden;
    }

    /* 도면 뒷 배경 격자 선 (검은색 가로줄) */
    .bg-lines {
        position: absolute; top: 0; left: 0; width: 100%; height: 100%; z-index: 1;
        background-image: 
            linear-gradient(to bottom, transparent 125px, #000 125px, #000 126.5px, transparent 126.5px),
            linear-gradient(to bottom, transparent 265px, #000 265px, #000 266.5px, transparent 266.5px);
    }

    .row-cont { display: flex; justify-content: center; position: relative; z-index: 2; margin-bottom: -15px; }
    .zigzag { margin-left: 135px; } /* 지그재그 오프셋 */

    /* 동그라미 카드 */
    .circle {
        border: 1.5px solid #000; border-radius: 50%; width: 125px; height: 125px;
        display: flex; flex-direction: column; justify-content: center; align-items: center;
        background-color: white; margin: 4px; flex-shrink: 0; box-shadow: 1px 1px 3px rgba(0,0,0,0.1);
    }
    
    /* 텍스트 스타일 */
    .p-n { font-weight: bold; font-size: 17px; margin-top: 5px; } /* 품목명 */
    .p-q { font-size: 21px; font-weight: 900; color: #000; margin: 1px 0; } /* 수량 */
    .p-l { color: #8eb44e; font-size: 15px; font-weight: bold; } /* 위치코드 (연두색) */
    
    /* 색상 구분 */
    .t-blue { color: #0000FF; } /* WASW 등 */
    .t-orange { color: #d35400; } /* WNS, WUR 등 */
    .zero-bg { background-color: #fff1f0; } /* 수량 0일 때 */
    .zero-bg .p-q { color: red; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">일 일 재 고 현 황 표</div>', unsafe_allow_html=True)

# 3. 데이터 초기화 (35개 행)
if 'inven' not in st.session_state:
    st.session_state['inven'] = pd.DataFrame({
        "품목명": ["WASW", "WCRS", "WASW", "WASWP", "WUR", "WNS"] + [""] * 29,
        "수량": [1508, 1671, 1754, 1496, 1494, 1686] + [0] * 29,
        "위치코드": ["A101", "A102", "A103", "A104", "A105", "A106"] + [f"A{i}" for i in range(201, 230)]
    })

# 4. 입력 표
with st.expander("📝 데이터 입력/수정 (클릭)"):
    edited_df = st.data_editor(st.session_state['inven'], num_rows="fixed", use_container_width=True)
    if st.button("수정 내용 적용하기"):
        st.session_state['inven'] = edited_df
        st.rerun()

st.divider()

# 5. 도면형 현황판 출력 (7개씩 5줄 지그재그)
df = st.session_state['inven']
st.markdown('<div class="main-container"><div class="bg-lines"></div>', unsafe_allow_html=True)

for r in range(5):
    zz_cls = "zigzag" if r % 2 != 0 else ""
    row_html = f'<div class="row-cont {zz_cls}">'
    
    sub_df = df.iloc[r*7 : (r+1)*7]
    for _, row in sub_df.iterrows():
        nm = str(row["품목명"]) if row["품목명"] else "-"
        lc = str(row["위치코드"]) if row["위치코드"] else ""
        try: qt = int(row["수량"])
        except: qt = 0
        
        # 품목명에 따른 색상 적용 (오른쪽 사진 기준)
        color_cls = "t-orange" if any(x in nm for x in ["WNS", "WCRS", "WUR"]) else "t-blue"
        bg_cls = "zero-bg" if qt == 0 else ""
        
        row_html += f"""
        <div class="circle {bg_cls}">
            <div class="p-n {color_cls}">{nm}</div>
            <div class="p-q">{qt:,}</div>
            <div class="p-l">{lc}</div>
        </div>"""
    
    row_html += '</div>'
    st.markdown(row_html, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
