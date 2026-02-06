import streamlit as st
import pandas as pd

# 1. 페이지 설정 (넓은 화면 사용)
st.set_page_config(page_title="일일 재고 현황표", layout="wide")

# 2. 가로 배치 및 지그재그 전용 CSS 디자인
st.markdown("""
<style>
    .title { text-align: center; font-size: 3em; font-weight: bold; text-decoration: underline; margin-bottom: 30px; }
    .main-board { display: flex; flex-direction: column; align-items: center; width: 100%; }
    
    /* 한 줄(7개)을 가로로 묶어주는 컨테이너 */
    .row-container { 
        display: flex; 
        flex-direction: row; 
        justify-content: center; 
        width: 100%; 
        margin-bottom: -45px; 
    }
    
    /* 지그재그 효과 (줄마다 엇갈림) */
    .zigzag { margin-left: 140px; } 

    .stock-card {
        border: 2.5px solid #333; border-radius: 50%; 
        width: 130px; height: 130px;
        display: flex; flex-direction: column; justify-content: center; align-items: center;
        background-color: white; margin: 10px; flex-shrink: 0;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    }
    .p-name { font-
