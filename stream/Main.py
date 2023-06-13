import streamlit as st
import os

from api.database import initCSV

st.set_page_config(
    page_title="Main",
    page_icon="👋",
)

dbDict = {
    'sns_ad.csv': ['제품 이름', '제품 정보', '필수 키워드',
                   '옵션 키워드', '추가 요구사항', '생성 문구 수']
}

initCSV(dbDict)

# st.write(os.getcwd())
# st.write(os.listdir(os.getcwd()))

st.write("# Welcome to CopyAssistant! 👋")

st.markdown(
    """
    저희는 고려대학교 세종캠퍼스에서 ㈜퓨어 기업과 협업하여 마케팅 성과를 향상시키는 프로젝트를 진행 중에 있습니다.
    빅데이터 분석 기술을 활용하여 chat gpt를 활용하여 마케팅 문구를 만들어주는 플랫폼을 제작하였습니다.
"""
)
