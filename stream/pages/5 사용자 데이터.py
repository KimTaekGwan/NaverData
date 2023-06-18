import streamlit as st

import time
import numpy as np
import pandas as pd
from datetime import datetime

from api.database import update_in_csv

#############################################


def layout_table(layout_1, table_name, path):
    with layout_1[0]:
        st.markdown(f"## {table_name}")
    sns_ad = pd.read_csv(path)
    sns_ad = st.data_editor(sns_ad)
    with layout_1[1]:
        col1, col2 = st.columns((1, 1))
        with col2:
            btn_update = st.button('업데이트', key=f'btn_{table_name}')
        with col1:
            if btn_update:
                update_in_csv(sns_ad, path)
                now = datetime.now()
                st.caption(f'{now.strftime("%Y-%m-%d %H:%M:%S")}')


#############################################
page_title = '사용자 데이터'
page_icon = '🗂️'

st.set_page_config(page_title=page_title,
                   layout='wide',
                   page_icon=page_icon
                   )

#############################################
# 제목
st.markdown(f"# {page_title} {page_icon}")


#############################################
# 본문
tab1, tab2, tab3 = st.tabs(["😃 SNS 광고문구", "📨 SMS 프로모션", "📢 앱 푸쉬 알림 멘트"])
with tab1:
    layout_1 = st.columns((3, 1))
    layout_table(layout_1, 'SNS 광고문구', 'sns_ad.csv')
with tab2:
    layout_2 = st.columns((3, 1))
    layout_table(layout_2, 'SMS 프로모션', 'sms_promotion.csv')
with tab3:
    layout_3 = st.columns((3, 1))
    layout_table(layout_3, '앱 푸쉬 알림 멘트', 'push_alarm.csv')
