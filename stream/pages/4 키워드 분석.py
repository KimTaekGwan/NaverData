import streamlit as st
import streamlit.components.v1 as components

import time
import numpy as np
import pandas as pd
import os

from api.database import html_loader

# Input Layout 생성


def createInputLayout(elements):

    # st.markdown(html, unsafe_allow_html=True)
    components.html(keyword_html, height=600)


#############################################
page_title = '키워드 분석 인사이트'
page_icon = '🍒'

st.set_page_config(page_title=page_title,
                   layout='wide',
                   page_icon=page_icon
                   )

last_params = {

}
elements = last_params.copy()

html_info = {
    'path': 'keywords.html',
    'url': 'https://raw.githubusercontent.com/KimTaekGwan/NaverData/main/stream/keywords.html'
}

keyword_html = html_loader(html_info)

#############################################
# 제목
st.markdown(f"# {page_title} {page_icon}")
st.write(os.getcwd())
st.markdown("""> 네이버 데이터랩 인기검색어의 경쟁사 제품 리뷰 데이터를 분석해 네트워크 그래프로 나타냈습니다. \n> 주요 키워드 연관어를 추출하고 Copy Assistant로 제작할 광고 문구의 필수 키워드 데이터를 얻을 수 있습니다.""")


#############################################
# 사이드바

#############################################
# 본문

# html layout
createInputLayout(elements)
