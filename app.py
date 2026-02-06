import streamlit as st
import pandas as pd

# 1. 페이지 설정
st.set_page_config(page_title="일일 재고 현황표", layout="wide")

# 2. 이미지와 똑같은 지그재그 그리드 디자인 (CSS)
st.markdown("""
<style>
    .title { text-align: center; font-size: 4em; font-weight: bold; text-decoration: underline; margin-bottom: 50px; font-family: 'serif'; }
    
    /* 전체 판을 감싸는 컨테이너 */
    .board-container {
        position: relative;
        background-color: white;
        padding: 50px 20px;
        display: flex;
        flex-direction: column;
        align-items: center;
        border-top: 2px solid #000;
        border-bottom: 2px solid #000;
    }

    /* 가로 줄 (Row) */
    .stock-row {
        display: flex;
        justify-content: center;
        width: 100%;
        margin-bottom: -40px; /* 줄 사이 간격을 좁혀서 지그재그 효과 */
    }

    /* 지그재그를 위해 홀수 줄에 왼쪽 여백 추가 */
    .row-offset {
        padding-left: 100px;
    }

    /* 동그라미 카드 스타일 */
    .stock-card {
        border: 1.5px solid #333;
        border-radius: 50%;
        width: 130px;
        height: 130px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        background-color: white;
        margin: 5px;
        z-index: 2;
    }

    /* 카드 내부 텍스트 설정 */
    .item-name { font-weight: bold; color: #0000FF; font-size: 1em; margin-top: 5px; }
    .item-qty { font-size: 1.3em; font-weight: bold; color: #000
