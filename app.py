import streamlit as st
import sqlite3
import pandas as pd

# --- 데이터베이스 설정 ---
def init_db():
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS inventory
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  item_name TEXT, 
                  quantity INTEGER, 
                  location TEXT)''') # '위치(코드)' 칸 추가
    conn.commit()
    conn.close()

init_db()

# --- 화면 스타일 설정 (이미지 느낌 내기) ---
st.markdown("""
    <style>
    .stock-card {
        border: 2px solid #333;
        border-radius: 50%;
        width: 150px;
        height: 150px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        margin: 10px;
        background-color: white;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
        text-align: center;
    }
    .item-name { font-weight: bold; color: blue; font-size: 1.1em; }
    .item-qty { font-size: 1.5em; font-weight: bold; margin: 5px 0; }
    .item-loc { color: #88bb88; font-size: 0.9em; }
    .low-stock { background-color: #ffebee; border-color: red; }
    .low-stock .item-qty { color: red; }
    </style>
    """, unsafe_allow_html=True)

st.title("📊 일일 재고 현황판")

# --- 입력 부분 (사이드바) ---
st.sidebar.header("📝 재고 입력/수정")
with st.sidebar.form("input_form"):
    name = st.text_input("품목명 (예: WASW)")
    qty = st.number_input("수량", min_value=0, step=1)
    loc = st.text_input("위치 코드 (예: A101)")
    submit = st.form_submit_button("장부에 기록")

if submit:
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()
    c.execute("SELECT * FROM inventory WHERE item_name=?", (name,))
    if c.fetchone():
        c.execute("UPDATE inventory SET quantity=?, location=? WHERE item_name=?", (qty, loc, name))
    else:
        c.execute("INSERT INTO inventory (item_name, quantity, location) VALUES (?, ?, ?)", (name, qty, loc))
    conn.commit()
    conn.close()
    st.rerun()

# --- 화면 출력 (대시보드 형태) ---
conn = sqlite3.connect('inventory.db')
df = pd.read_sql_query("SELECT * FROM inventory", conn)
conn.close()

if not df.empty:
    # 6개씩 한 줄에 배치 (이미지와 유사하게)
    cols = st.columns(6)
    for idx, row in df.iterrows():
        with cols[idx % 6]:
            # 수량이 0이면 빨간색 스타일 적용
            card_class = "stock-card low-stock" if row['quantity'] == 0 else "stock-card"
            
            st.markdown(f"""
                <div class="{card_class}">
                    <div class="item-name">{row['item_name']}</div>
                    <div class="item-qty">{row['quantity']:,}</div>
                    <div class="item-loc">{row['location']}</div>
                </div>
                """, unsafe_allow_html=True)
else:
    st.info("왼쪽에서 재고를 먼저 입력해 주세요!")

# 삭제 기능은 하단에 작게 배치
st.divider()
if not df.empty:
    with st.expander("🗑️ 품목 삭제하기"):
        del_item = st.selectbox("삭제할 품목", df['item_name'].tolist())
        if st.button("삭제 실행"):
            conn = sqlite3.connect('inventory.db')
            c = conn.cursor()
            c.execute("DELETE FROM inventory WHERE item_name=?", (del_item,))
            conn.commit()
            conn.close()
            st.rerun()
