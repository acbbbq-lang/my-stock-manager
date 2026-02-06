import streamlit as st
import pandas as pd

# 1. 페이지 설정
st.set_page_config(page_title="일일 재고 현황표", layout="wide")

# 2. 도면 스타일 CSS (배경 선 및 지그재그 정렬)
st.markdown("""
<style>
    .title { text-align: center; font-size: 3em; font-weight: bold; text-decoration: underline; margin-bottom: 20px; }
    .main-board { 
        position: relative; width: 1100px; margin: 0 auto; padding: 40px 0;
        background-color: white; border: 1px solid #ccc;
    }
    /* 도면 뒷 배경 가로선 */
    .bg-lines {
        position: absolute; top: 0; left: 0; width: 100%; height: 100%; z-index: 1;
        background-image: linear-gradient(to bottom, transparent 115px, #333 115px, #333 116px, transparent 116px, 
                          transparent 245px, #333 245px, #333 246px, transparent 246px);
    }
    .row-cont { display: flex; justify-content: center; position: relative; z-index: 2; margin-bottom: -10px; }
    .zigzag { margin-left: 140px; } 
    .circle {
        border: 2px solid #000; border-radius: 50%; width: 125px; height: 125px;
        display: flex; flex-direction: column; justify-content: center; align-items: center;
        background-color: white; margin: 5px; flex-shrink: 0; box-shadow: 1px 1px 3px rgba(0,0,0,0.2);
    }
    .p-n { font-weight: bold; font-size: 16px; margin-top: 5px; }
    .p-q { font-size: 20px; font-weight: 900; color: black; margin: 2px 0; }
    .p-l { color: #8eb44e; font-size: 14px; font-weight: bold; }
    /* 품목별 색상 */
    .blue-t { color: #0000FF; }
    .orange-t { color: #d35400; }
    .zero { background-color: #fff1f0; }
    .zero .p-q { color: red; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">일 일 재 고 현 황 표</div>', unsafe_allow_html=True)

# 3. 데이터 초기화 (35개 항목)
if 'inven' not in st.session_state:
    st.session_state['inven'] = pd.DataFrame({
        "품목명": ["WASW", "WCRS", "WASW", "WASWP", "WUR", "WNS"] + [""] * 29,
        "수량": [1508, 1671, 1754, 1496, 1494, 1686] + [0] * 29,
        "위치코드": ["A101", "A102", "A103", "A104", "A105", "A106"] + [f"A{i}" for i in range(107, 136)]
    })

# 4. 데이터 입력 표 (접기 기능)
with st.expander("📝 데이터 수정하기 (여기를 클릭)"):
    edited_df = st.data_editor(st.session_state['inven'], num_rows="fixed", use_container_width=True)
    if st.button("수정 내용 적용"):
        st.session_state['inven'] = edited_df
        st.rerun()

st.divider()

# 5. 현황판 출력 (지그재그 7x5)
df = st.session_state['inven']
st.markdown('<div class="main-board"><div class="bg-lines"></div>', unsafe_allow_html=True)

for r in range(5):
    zz = "zigzag" if r % 2 != 0 else ""
    row_html = f'<div class="row-cont {zz}">'
    
    sub_df = df.iloc[r*7 : (r+1)*7]
    for _, row in sub_df.iterrows():
        nm = str(row["품목명"]) if row["품목명"] else "-"
        lc = str(row["위치코드"]) if row["위치코드"] else ""
        try: qt = int(row["수량"])
        except: qt = 0
        
        # 품목명 색상 결정
        c_style = "orange-t" if any(x in nm for x in ["WNS", "WCRS", "WUR"]) else "blue-t"
        bg_cls = "zero" if qt == 0 else ""
        
        row_html += f"""
        <div class="circle {bg_cls}">
            <div class="p-n {c_style}">{nm}</div>
            <div class="p-q">{qt:,}</div>
            <div class="p-l">{lc}</div>
        </div>"""
    
    row_html += '</div>'
    st.markdown(row_html, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
