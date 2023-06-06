import streamlit as st
from streamlit_tags import st_tags  # , st_tags_sidebar

import time
import numpy as np
import pandas as pd

from api.gpt import CopyWriter

st.set_page_config(page_title="SNS 광고문구", page_icon="📈")

st.markdown("# SNS 광고문구")
st.markdown("> 소비자가 열광할 메타 (페이스북, 인스타그램) 광고의 내용을 생성해보세요.")

# product 입력
st.markdown("### 제품 이름")
product = st.text_input(
    label='제품 이름',
    value='엘더하이 젤리',
    placeholder='홍보하려는 제품 이름을 작성해 주세요.(최대 20자)',

    max_chars=20,
    disabled=False,
    label_visibility='collapsed'  # "visible", "hidden", "collapsed"
)

# description 입력
st.markdown("### 제품 설명")
description = st.text_input(
    label='제품 간단 정보',
    value='기존 엘더하이 음료수 제품을 젤리 형태로 신제품 출시. 영양흡수율 증가 기수을 활용하여 제품 사용자인 영유아(2세~7세)에게 면역력을 향상 시키는 것을 목적',
    placeholder='소개하려는 제품 정보를 간략하게 작성해 주세요.(최대 100자)',
    max_chars=100,
    disabled=False,
    label_visibility='collapsed'  # "visible", "hidden", "collapsed"
)

# keywords 입력
st.markdown("### 포함 키워드")
keywords = st.text_input(
    label='포함 키워드',
    value='엘더하이 젤리 유치원집 면역력 휴대',
    placeholder='각 키워드는 단어의 조합으로 입력해 주세요.',
    max_chars=100,
    disabled=False,
    label_visibility='collapsed'  # "visible", "hidden", "collapsed"
)

# 문구 수 입력
num_copy = st.number_input(
    label='추천 문구 수',
    min_value=1,
    max_value=10,
    value=5,
    step=1
)

st.write(f'제품 이름: :violet[{product}]')
st.write(f'제품 정보: :violet[{description}]')
st.write(f'포함 키워드: :violet[{set(keywords.split())}]')
st.write(f'추천 문구 수: :violet[{num_copy}]')


button = st.button('주제 생성')
if button:
    wrtier = CopyWriter()

    res = wrtier.process_run(
        product, description, keywords, num_copy)
    st.write(f'{res}')
    # st.write(f'추천 문구 수: :violet[{res}]')
