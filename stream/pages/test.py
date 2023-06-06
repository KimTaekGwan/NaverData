import streamlit as st

import time
import numpy as np
import pandas as pd

from api.gpt import Brainstoming

st.set_page_config(page_title="Plotting Demo", page_icon="📈")

st.markdown("# Plotting Demo")
st.sidebar.header("Plotting Demo")
st.write(
    """This demo illustrates a combination of plotting and animation with
Streamlit. We're generating a bunch of random numbers in a loop for around
5 seconds. Enjoy!"""
)

data_infos = {
    12345: {
        'data_name': 'iris',
        'data_description': '붓꽃 데이터셋',
        'columns': [
            {'column_name': 'sepal_length', 'column_description': '꽃받침 길이'},
            {'column_name': 'sepal_width', 'column_description': '꽃받침 너비'},
            {'column_name': 'petal_length', 'column_description': '꽃잎 길이'},
            {'column_name': 'petal_width', 'column_description': '꽃잎 너비'},
            {'column_name': 'class', 'column_description': '붓꽃 종류'}
        ]
    },
    12346: {
        'data_name': 'titanic',
        'data_description': '타이타닉 호 생존자 데이터',
        'columns': [
            {'column_name': 'survived',
             'column_description': '생존 여부 (0: 사망, 1: 생존)'},
            {'column_name': 'pclass',
             'column_description': '선실 등급 (1, 2, 3 중 하나)'},
            {'column_name': 'sex', 'column_description': '성별'},
            {'column_name': 'age', 'column_description': '나이'},
            {'column_name': 'fare', 'column_description': '운임'},
            {'column_name': 'embarked',
             'column_description': '승선 항구 (C = Cherbourg, Q = Queenstown, S = Southampton)'}
        ]
    }
}

# 선택 박스
mbti = st.selectbox(
    '당신의 MBTI는 무엇입니까?',
    ('ISTJ', 'ENFP', '선택지 없음'),
    index=2
)

if mbti == 'ISTJ':
    st.write('당신은 :blue[현실주의자] 이시네요')
elif mbti == 'ENFP':
    st.write('당신은 :green[활동가] 이시네요')
else:
    st.write("당신에 대해 :red[알고 싶어요]:grey_exclamation:")

button = st.button('로또를 생성해 주세요!')
if button:
    field = '교육'
    purpose = '머신러닝 연습'
    num_topics = 5

    brain = Brainstoming()

    res = brain.process_run(data_infos, field, purpose, num_topics)

    st.write('당신이 입력하신 나이는:  ', res)
