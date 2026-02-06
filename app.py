import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime

# --- 1. 데이터베이스(장부) 설정 ---
# 이 부분은 'inventory.db'라는 장부 파일을 만들고 데이터를 저장하는 규칙을 정합니다.
def init_db():
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS inventory
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  item_name TEXT, 
                  quantity INTEGER, 
                  last_updated TEXT)''')
    conn.commit()
    conn.close()

# 데이터 불러오기 함수
def load_data():
    conn = sqlite3.connect('inventory.db')
    df = pd.read_sql_query("SELECT * FROM inventory", conn)
    conn.close()
    return df

# 데이터 추가/수정 함수
def update_item(name, qty):
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # 이미 있는 품목인지 확인
    c.execute("SELECT * FROM inventory WHERE item_name=?", (name,))
    data = c.fetchone()
    
    if data:
        c.execute("UPDATE inventory SET quantity=?, last_updated=? WHERE item_name=?", (qty, now, name))
    else:
        c.execute("INSERT INTO inventory (item_name, quantity, last_updated) VALUES (?, ?, ?)", (name, qty, now))
    
    conn.commit()
    conn.close()

# --- 2. 웹 화면 꾸미기 (UI) ---
st.set_page_config(page_title="나의 일일 재고표", layout="wide")
init_db()

st.title("📦 초간편 일일 재고 관리 시스템")
st.write("품목을 입력하고 수량을 조절해 보세요. 데이터는 자동으로 저장됩니다.")

# 사이드바: 입력 창
st.sidebar.header("📝 품목 등록/수정")
item_name = st.sidebar.text_input("품목 이름 (예: 사과)")
item_qty = st.sidebar.number_input("현재 수량", min_value=0, value=0, step=1)

if st.sidebar.button("장부에 기록하기"):
    if item_name:
        update_item(item_name, item_qty)
        st.sidebar.success(f"'{item_name}' 기록 완료!")
        st.rerun() # 화면 새로고침
    else:
        st.sidebar.error("품목 이름을 입력해주세요.")

# 메인 화면: 재고 표 보여주기
st.subheader("📊 현재 재고 현황")
df = load_data()

if not df.empty:
    # 표 디자인 예쁘게 출력
    st.dataframe(df[['item_name', 'quantity', 'last_updated']], 
                 column_config={
                     "item_name": "품목명",
                     "quantity": "현재 수량",
                     "last_updated": "최종 업데이트"
                 },
                 use_container_width=True)
    
    # 선택 삭제 기능
    st.divider()
    delete_target = st.selectbox("삭제할 품목 선택", df['item_name'].tolist())
    if st.button("선택한 품목 삭제"):
        conn = sqlite3.connect('inventory.db')
        c = conn.cursor()
        c.execute("DELETE FROM inventory WHERE item_name=?", (delete_target,))
        conn.commit()
        conn.close()
        st.warning(f"'{delete_target}' 삭제되었습니다.")
        st.rerun()
else:
    st.info("아직 등록된 재고가 없습니다. 왼쪽 메뉴에서 첫 품목을 등록해 보세요!")