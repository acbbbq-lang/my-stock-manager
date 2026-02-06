import streamlit as st
import pandas as pd
import sqlite3

# --- 화면 스타일 설정 (이미지 디자인 재현) ---
st.set_page_config(page_title="일일 재고 현황표", layout="wide")

st.markdown("""
    <style>
    .title { text-align: center; font-size: 3em; font-weight: bold; text-decoration: underline; margin-bottom: 50px; }
    .stock-container { display: flex; flex-wrap: wrap; justify-content: center; background-color: white; padding: 20px; border: 1px solid #ccc; }
    .stock-card {
        border: 1px solid #333;
        border-radius: 50%;
        width: 130px;
        height: 130px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        margin: 15px;
        text-align: center;
        background-color: white;
    }
    .item-name { font-weight: bold; color: #0000FF; font-size: 1.1em; }
    .item-qty { font-size: 1.3em; font-weight: bold; margin: 2px 0; color: #000; }
    .item-loc { color: #99cc99; font-size: 0.85em; }
    .low-stock { background-color: #ffebee; border-color: #ff0000; }
    .low-stock .item-qty { color: #ff0000; }
    </style>
    """, unsafe_allow_html=True)

# --- 데이터베이스 함수 ---
def save_to_db(df):
    conn = sqlite3.connect('inventory.db')
    df.to_sql('inventory', conn, if_exists='replace', index=False)
    conn.commit()
    conn.close()

def load_from_db():
    conn = sqlite3.connect('inventory.db')
    try:
        df = pd.read_sql_query("SELECT * FROM inventory", conn)
    except:
        df = pd.DataFrame(columns=['item_name', 'quantity', 'location'])
    conn.close()
    return df

# --- 메인 화면 ---
st.markdown('<div class="title">일 일 재 고 현 황 표</div>', unsafe_allow_html=True)

# 사이드바: 엑셀 업로드
st.sidebar.header("📁 데이터 업데이트")
uploaded_file = st.sidebar.file_ acorns_uploader("엑셀 파일 업로드 (.xlsx)", type=["xlsx"])

if uploaded_file:
    try:
        new_data = pd.read_excel(uploaded_file)
        # 필수 컬럼 확인
        if all(col in new_data.columns for col in ['item_name', 'quantity', 'location']):
            save_to_db(new_data)
            st.sidebar.success("엑셀 데이터 반영 완료!")
        else:
            st.sidebar.error("엑셀 헤더를 확인하세요: item_name, quantity, location")
    except Exception as e:
        st.sidebar.error(f"에러 발생: {e}")

# 데이터 불러오기
df = load_from_db()

# 현황판 출력
if not df.empty:
    # 이미지처럼 격자 형태로 배치하기 위해 컨테이너 생성
    st.markdown('<div class="stock-container">', unsafe_allow_html=True)
    
    # 한 줄에 6개씩 배치
    rows = [df[i:i + 6] for i in range(0, len(df), 6)]
    
    for row_data in rows:
        cols = st.columns(6)
        for i, (idx, item) in enumerate(row_data.iterrows()):
            with cols[i]:
                # 수량이 0인 경우 빨간색 강조
                is_low = "low-stock" if item['quantity'] == 0 else ""
                st.markdown(f"""
                    <div class="stock-card {is_low}">
                        <div class="item-name">{item['item_name']}</div>
                        <div class="item-qty">{int(item['quantity']):,}</div>
                        <div class="item-loc">{item['location']}</div>
                    </div>
                """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.info("왼쪽 사이드바에서 엑셀 파일을 업로드하면 현황표가 나타납니다.")

