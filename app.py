import streamlit as st
import pandas as pd

# 1. 페이지 설정
st.set_page_config(page_title="일일 재고 현황표", layout="wide")

# 2. 도면 스타일 CSS (오른쪽 그림과 100% 일치하도록 수정)
st.markdown("""
<style>
    .title { text-align: center; font-size: 3.5em; font-weight: bold; text-decoration: underline; margin-bottom: 20px; font-family: 'serif'; }
    
    /* 도면 전체 컨테이너: 상단 여백 제거 및 테두리 설정 */
    .main-container {
        position: relative; 
        width: 1050px; 
        margin: 0 auto; 
        padding: 20px 0px; /* 상단 네모 공간 제거를 위해 패딩 조절 */
        background-color: white; 
        border: 1px solid #000;
        z-index: 0;
    }

    /* 도면 뒷 배경 가로선: 오른쪽 그림의 선 위치와 두께 재현 */
    .bg-lines {
        position: absolute; top: 0; left: 0; width: 100%; height: 100%; z-index: -1;
        background-image: 
            linear-gradient(to bottom, 
                transparent 85px, #000 85px, #000 86.5px, transparent 86.5px,
                transparent 220px, #000 220px, #000 221.5px, transparent 221.5px,
                transparent 355px, #000 355px, #000 356.5px, transparent 356.5px
            );
    }

    .row-cont { display: flex; justify-content: center; position: relative; margin-bottom: -10px; }
    .zigzag { margin-left: 140px; } /* 지그재그 엇갈림 효과 */

    /* 동그라미 카드 디자인 */
    .circle {
        border: 1.5px solid #000; border-radius: 50%; 
        width: 125px; height: 125px;
        display: flex; flex-direction: column; justify-content: center; align-items: center;
        background-color: white; margin: 5px; flex-shrink: 0;
        box-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }
    
    /* 텍스트 스타일: 오른쪽 그림 색상 반영 */
    .p-n { font-weight: bold; font-size: 16px; margin-bottom: 2px; } /* 품목명 */
    .p-q { font-size: 20px; font-weight: 900; color: #000; margin: 0; } /* 수량 */
    .p-l { color: #8eb44e; font-size: 14px; font-weight: bold; } /* 위치코드 (연두색) */
    
    /* 품목별 글자 색상 */
    .t-blue { color: #0000FF; } /* WASW 등 파란색 */
    .t-orange { color: #d35400; } /* WNS, WUR 등 주황색 */
    
    /* 수량 0일 때 배경 강조 */
    .zero-bg { background-color: #fff1f0; border-color: #ffcccc; }
    .zero-bg .p-q { color: red; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">일 일 재 고 현 황 표</div>', unsafe_allow_html=True)

# 3. 데이터 초기화 (35개 항목)
if 'inven' not in st.session_state:
    st.session_state['inven'] = pd.DataFrame({
        "품목명": ["WASW", "WCRS", "WASW", "WASWP", "WUR", "WNS"] + ["-"] * 29,
        "수량": [1508, 1671, 1754, 1496, 1494, 1686] + [0] * 29,
        "위치코드": ["A101", "A102", "A103", "A104", "A105", "A106"] + [f"A{i}" for i in range(201, 230)]
    })

# 4. 상단 입력 표 (데이터 수정용)
with st.expander("📝 데이터 입력 및 수정"):
    edited_df = st.data_editor(st.session_state['inven'], num_rows="fixed", use_container_width=True)
    if st.button("수정 내용 적용하기"):
        st.session_state['inven'] = edited_df
        st.rerun()

st.divider()

# 5. 오른쪽 도면 구현 (7개씩 5줄 지그재그)
df = st.session_state['inven']
st.markdown('<div class="main-container"><div class="bg-lines"></div>', unsafe_allow_html=True)

for r in range(5):
    zz_cls = "zigzag" if r % 2 != 0 else ""
    row_html = f'<div class="row-cont {zz_cls}">'
    
    sub_df = df.iloc[r*7 : (r+1)*7]
    for _, row in sub_df.iterrows():
        nm = str(row["품목명"])
        lc = str(row["위치코드"])
        try: qt = int(row["수량"])
        except: qt = 0
        
        # 글자 색상 로직: 특정 단어가 포함되면 주황색, 아니면 파란색
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
