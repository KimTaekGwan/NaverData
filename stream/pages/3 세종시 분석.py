import streamlit as st
import streamlit.components.v1 as components

from api.database import html_loader

import time
import numpy as np
import pandas as pd


# Input Layout 생성
def createInputLayout(elements):

    # st.markdown(html, unsafe_allow_html=True)
    components.html(sejong_html, height=600)


#############################################
page_title = '세종시 분석 인사이트'
page_icon = '😃'

st.set_page_config(page_title=page_title,
                   layout='wide',
                   page_icon=page_icon
                   )

last_params = {

}
elements = last_params.copy()

html_info = {
    'path': 'sejong_insight.html',
    'url': 'https://raw.githubusercontent.com/KimTaekGwan/NaverData/main/stream/sejong_insight.html'
}

sejong_html = html_loader(html_info)

# print(html)


#############################################
# 제목
st.markdown(f"# {page_title} {page_icon}")
st.markdown("> 소비자가 열광할 메타 (페이스북, 인스타그램) 광고의 내용을 생성해보세요.")


#############################################
# 사이드바

#############################################
# 본문

# html layout
createInputLayout(elements)
