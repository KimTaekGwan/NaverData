import streamlit as st
import os

from api.database import initCSV

st.set_page_config(
    page_title="Main",
    page_icon="👋"
    # layout="wide"
)

dbDict = {
    'sns_ad.csv': ['제품 이름', '제품 정보', '필수 키워드',
                   '옵션 키워드', '추가 요구사항', '생성 문구 수']
}

initCSV(dbDict)

# st.write(os.getcwd())
# st.write(os.listdir(os.getcwd()))

st.write("# Welcome to CopyAssistant! 👋")

st.markdown('안녕하세요!')

st.markdown("""저희는 고려대학교 세종캠퍼스 캡스톤디자인 수업에서\n
푸드테크 기업 (주)퓨어의 업무 프로세스 향상을 위한 프로젝트를 진행중입니다.\n
생성 AI를 활용하여 마케팅 문구를 만들어주는 플랫폼을 제작했습니다.
""")
