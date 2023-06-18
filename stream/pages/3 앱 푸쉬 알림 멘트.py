import streamlit as st

import time
import numpy as np
import pandas as pd
# from collections import defaultdict

from api.gpt import CopyWriter
from api.util import update_param
from api.database import insert_row_in_csv


#############################################
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


# Input Layout 생성
def createInputLayout(elements):

    # 전달한 내용 입력
    st.markdown("### 전달한 내용")
    elements['전달한 내용'] = st.empty()
    elements['전달한 내용'].text_input(
        label='전달한 내용',
        key='전달한 내용',
        value='6월 2주차 업데이트 공지',
        placeholder='전달한 내용을 간략히 작성해 주세요.',
        max_chars=50,
        disabled=False,
        label_visibility='collapsed'  # "visible", "hidden", "collapsed"
    )

    # 필수 키워드 입력
    st.markdown("### 필수 키워드")
    elements['필수 키워드'] = st.empty()
    elements['필수 키워드'].text_input(
        label='필수 키워드',
        key='필수 키워드',
        value='엘더하이 젤리 제품 입고',
        placeholder='전하고자 하는 핵심 내용을 키워드 형식으로 작성해 주세요.',
        max_chars=50,
        disabled=False,
        label_visibility='collapsed'
    )

    # st.markdown("### 옵션")
    with st.expander("추가 옵션"):
        # opt_keywords 입력
        st.markdown("#### 옵션 키워드")
        elements['옵션 키워드'] = st.empty()
        elements['옵션 키워드'].text_input(
            label='옵션 키워드',
            key='옵션 키워드',
            value='X',
            placeholder='각 키워드는 단어의 조합으로 입력해 주세요.',
            max_chars=50,
            disabled=False,
            label_visibility='collapsed'
        )

    # 생성 문구 수
    st.markdown("### 생성 문구 수")
    elements['생성 문구 수'] = st.empty()
    elements['생성 문구 수'].number_input(
        label='생성 문구 수',
        key='생성 문구 수',
        min_value=2,
        max_value=10,
        value=3,
        label_visibility='collapsed',
        step=1
    )

    # add_data = st.button('데이터 추가')
    # if add_data:
    if st.button('데이터 추가'):
        update_params()
        insert_row_in_csv(path, last_params)

    with st.expander("현재 입력 정보"):
        displayINPUT()


def updateINPUT(load_dict):
    for k, v in load_dict.items():
        st.session_state[k] = v


#############################################
page_title = '앱 푸쉬 알림 멘트'
page_icon = '📢'

st.set_page_config(page_title=page_title,
                   layout='wide',
                   page_icon=page_icon
                   )

last_params = {
    '전달한 내용': None,
    '필수 키워드': None,
    '옵션 키워드': None,
    '생성 문구 수': None
}
elements = last_params.copy()

wrtier = CopyWriter(page_num=3)
path = 'push_alarm.csv'
df = pd.read_csv(path)


#############################################
# 제목
st.markdown(f"# {page_title} {page_icon}")
st.markdown("> 클릭하고 싶게 만드는 푸쉬 알림 멘트를 작성해 보세요.")


#############################################
# 사이드바

btn_load = st.sidebar.button('데이터 불러오기')
if len(df) == 0:
    max_value = 0
else:
    row_num = st.sidebar.number_input(
        label='행번호',
        key='행번호',
        min_value=0,
        max_value=len(df)-1,
        value=0,
        label_visibility='collapsed',
        step=1
    )
    load_data = df.iloc[row_num, :].to_dict()
    st.sidebar.caption('\n\n'.join(
        [f'[{k}] {v}' for k, v in load_data.items()]))
    expander = st.sidebar.expander("데이터 확인하기")
    display_df = expander.dataframe(df)

    if btn_load:
        # print(df.iloc[row_num, :].to_dict())
        updateINPUT(load_data)

#############################################
# 본문

# InputLayout
createInputLayout(elements)

# OutputLayout
st.markdown("---")
btn_create = st.button('카피 생성')
tab1, tab2 = st.tabs(["생성 문구", "최종 입력 정보"])
with tab1:
    if btn_create:
        update_params()
        with st.spinner('Wait for it...'):
            res = wrtier.process_run(last_params)
            for i, topic in enumerate(res['data'], start=1):
                st.markdown(f'{i}. {topic}')
            st.caption(f'총 사용 토큰 수: {res["total_tokens"]}')

with tab2:
    if btn_create:
        displayINPUT(display=1)
