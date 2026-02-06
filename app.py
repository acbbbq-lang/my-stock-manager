import streamlit as st
import pandas as pd

# 1. 화면 설정 (광폭 레이아웃 사용)
st.set_page_config(page_title="일일 재고 현황표", layout="wide")

# 2. 디자인 스타일 (이미지 5a975b의 지그재그 가로 배치 재현)
st.markdown("""
<style>
    .title { text-align: center; font-size: 3.5em; font-weight: bold; text-decoration: underline; margin-bottom: 40px; }
    .board-container { display: flex; flex-direction: column; align-items: center; width: 100%; background-color: white; }
    
    /* 가로 배치를 위한 레이아웃 */
    .stock-row { display: flex; flex-direction: row; justify-content: center; width: 100%; margin-bottom: -45px; }
    .row-offset { margin-left: 140px; } /* 지그재그 밀기 효과 */
    
    .stock-card {
        border: 1.5px solid #333; border-radius: 50%; width: 130px; height: 130px;
        display: flex; flex-direction: column; justify-content: center; align-items: center;
        background-color: white; margin: 10px; z-index: 2;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    }
    .item-name { font-weight: bold; color: #0000FF; font-size: 0.95em; }
    .item-qty { font-size: 1.3em; font-weight: bold; color: #000; margin: 3px 0; }
    .item-loc { color: #8DB48E; font-size: 0.85em; font-weight: bold; }
    
    /* 수량 0일 때 스타일 */
    .out-of-stock { background-color: #FDF2F4; }
    .out-of-stock
