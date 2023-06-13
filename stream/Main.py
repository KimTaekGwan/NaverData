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

st.write(os.getcwd())
st.write(os.listdir(os.getcwd()))

st.write("# Welcome to Streamlit! 👋")

st.sidebar.success("Select a demo above.")

st.markdown(
    """
    Streamlit is an open-source app framework built specifically for
    Machine Learning and Data Science projects.
    **👈 Select a demo from the sidebar** to see some examples
    of what Streamlit can do!
    ### Want to learn more?
    - Check out [streamlit.io](https://streamlit.io)
    - Jump into our [documentation](https://docs.streamlit.io)
    - Ask a question in our [community
        forums](https://discuss.streamlit.io)
    ### See more complex demos
    - Use a neural net to [analyze the Udacity Self-driving Car Image
        Dataset](https://github.com/streamlit/demo-self-driving)
    - Explore a [New York City rideshare dataset](https://github.com/streamlit/demo-uber-nyc-pickups)
"""
)
