import streamlit as st

import time
import numpy as np
import pandas as pd
# from collections import defaultdict

from api.gpt import CopyWriter
from api.util import update_param

st.set_page_config(page_title="SNS 광고문구", page_icon="😃")


@st.cache_resource
def load_copywriter():
    return CopyWriter()


def displayINPUT(display=0):
    # 최종 입력 정보 출력 함수
    if display == 0:  # 현재
        st.markdown(f"### 현재 입력 정보")
        for key in last_params.keys():
            cond1 = st.session_state[key] != None
            cond2 = str(st.session_state[key]).strip() != ''
            if cond1 and cond2:
                st.write(f'{key}:\n\n :violet[{st.session_state[key]}]')
    else:          # 마지막 입력
        st.markdown(f"### 최종 입력 정보")
        for key, value in last_params.items():
            st.write(f'{key}:\n\n :violet[{value}]')


def update_params():
    for key in last_params.keys():
        cond1 = st.session_state[key] != None
        cond2 = str(st.session_state[key]).strip() != ''
        if cond1 and cond2:
            update_param(last_params, key, st.session_state[key])


last_params = {
    '제품 이름': None,
    '제품 이름': None,
    '필수 키워드': None,
    '옵션 키워드': None,
    '추가 요구사항': None,
    '제품 이름': None,
    '생성 문구 수': None
}

wrtier = load_copywriter()


# 제목
st.markdown("# SNS 광고문구 😃")
st.markdown("> 소비자가 열광할 메타 (페이스북, 인스타그램) 광고의 내용을 생성해보세요.")

# product 입력
st.markdown("### 제품 이름")
product = st.text_input(
    label='제품 이름',
    key='제품 이름',
    value='엘더하이 젤리',
    placeholder='홍보하려는 제품 이름을 작성해 주세요.(최대 20자)',
    max_chars=20,
    disabled=False,
    label_visibility='collapsed'  # "visible", "hidden", "collapsed"
)

# description 입력
st.markdown("### 제품 설명")
description = st.text_input(
    label='제품 정보',
    key='제품 정보',
    value='기존 엘더하이 음료수 제품을 젤리 형태로 신제품 출시. 영양흡수율 증가 기수을 활용하여 제품 사용자인 영유아(2세~7세)에게 면역력을 향상 시키는 것을 목적',
    placeholder='소개하려는 제품 정보를 간략하게 작성해 주세요.(최대 100자)',
    max_chars=100,
    disabled=False,
    label_visibility='collapsed'
)

# required_keywords 입력
st.markdown("### 필수 키워드")
req_keywords = st.text_input(
    label='필수 키워드',
    key='필수 키워드',
    value='엘더하이 젤리 면역력',
    placeholder='각 키워드는 단어의 조합으로 입력해 주세요.',
    max_chars=100,
    disabled=False,
    label_visibility='collapsed'
)


# st.markdown("### 옵션")
with st.expander("추가 옵션"):
    # opt_keywords 입력
    st.markdown("#### 옵션 키워드")
    opt_keywords = st.text_input(
        label='옵션 키워드',
        key='옵션 키워드',
        value='유치원집 휴대',
        placeholder='각 키워드는 단어의 조합으로 입력해 주세요.',
        max_chars=100,
        disabled=False,
        label_visibility='collapsed'
    )

    # add_req 입력
    st.markdown("#### 추가 요구사항")
    add_req = st.text_input(
        label='추가 요구사항',
        key='추가 요구사항',
        value='',
        placeholder='추가 요구사항을 작성해 주세요.',
        max_chars=100,
        disabled=False,
        label_visibility='collapsed'
    )

# 생성 문구 수
st.markdown("### 생성 문구 수")
num_copy = st.number_input(
    label='생성 문구 수',
    key='생성 문구 수',
    min_value=1,
    max_value=10,
    value=3,
    label_visibility='collapsed',
    step=1
)


with st.expander("현재 입력 정보"):
    displayINPUT()

st.markdown("---")

button = st.button('카피 생성')
tab1, tab2 = st.tabs(["생성 문구", "최종 입력 정보"])
with tab1:
    if button:
        update_params()
        with st.spinner('Wait for it...'):
            res = wrtier.process_run(last_params)
            for i, topic in enumerate(res['data'], start=1):
                st.markdown(f'{i}. {topic}')
            st.caption(f'총 사용 토큰 수: {res["total_tokens"]}')

with tab2:
    if button:
        displayINPUT(display=1)
