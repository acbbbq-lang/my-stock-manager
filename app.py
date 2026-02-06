import streamlit as st
import pandas as pd

# --- 화면 설정 ---
st.set_page_config(page_title="일일 재고 현황표", layout="wide")

# --- 디자인 스타일 (보내주신 이미지 재현) ---
st.markdown("""
    <style>
    .title { text-align: center; font-size: 3em; font-weight: bold; text-decoration: underline; margin-bottom: 30px; }
    .stock-container { display: flex; flex-wrap: wrap; justify-content: center; background-color: white; padding: 20px; border: 1px solid #ccc; }
    .stock-card {
        border: 1px solid #333;
        border-radius: 50%;
        width: 120px;
        height: 120px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        margin: 10px;
        text-align: center;
        background-color: white;
    }
    .item-name { font-weight: bold; color: #0000FF; font-size: 1em; }
    .item-qty { font-size: 1.2em; font-weight: bold; margin: 2px 0; color: #000; }
    .item-loc { color: #88bb88; font-size: 0.8em; }
    .low-stock { background-color: #ffebee; border-color: #ff0000; }
    .low-stock .item-qty { color: #ff0000; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="title">일 일 재 고 현 황 표</div>', unsafe_allow_html=True)

# --- 데이터 관리 (초기값) ---
if 'inventory_data' not in st.session_state:
    # 처음 접속했을 때 보여줄 예시 데이터
    st.session_state.inventory_data = pd.DataFrame([
        {"item_name": "WASW", "quantity": 1508, "location": "A101"},
        {"item_name": "WCRS", "quantity": 1671, "location": "A102"},
        {"item_name": "WASW", "quantity": 1754, "location": "A103"},
        {"item_name": "WASWP", "quantity": 1496, "location": "A104"},
        {"item_name": "WUR", "quantity": 1494, "location": "A105"},
        {"item_name": "WNS", "quantity": 1686, "location": "A106"}
    ])

# --- 1. 데이터 입력/수정 영역 ---
st.subheader
