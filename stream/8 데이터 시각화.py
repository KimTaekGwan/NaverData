# import streamlit as st

# import pandas as pd
# from pandasai import PandasAI
# from pandasai.llm.openai import OpenAI

# from api.gpt import getsecret
# import matplotlib

# matplotlib.use('TkAgg')

# # Input Layout 생성


# def createInputLayout(elements):
#     # 파일 업로드
#     file = st.file_uploader('파일 선택(csv or excel)',
#                             type=['csv', 'xls', 'xlsx'])

#     if file is not None:
#         # 파일 읽기
#         name, ext = file.name.split('.')[0], file.name.split('.')[-1]
#         if ext == 'csv':
#             # 파일 읽기
#             df = pd.read_csv(file)
#         elif 'xls' in ext:
#             df = pd.read_excel(file, engine='openpyxl')

#         with st.expander(f'데이터 프레임 미리보기 : {file.name}'):
#             st.dataframe(df.head())

#         elements['질문'] = st.empty()
#         elements['질문'].text_input(
#             label='질문',
#             key='질문',
#             value='',
#             placeholder='시각화하고 싶은 내용에 대해 입력해주세요.',
#             max_chars=100,
#             disabled=False,
#             label_visibility='collapsed'  # "visible", "hidden", "collapsed"
#         )

#         if st.button('시각화'):
#             cond1 = st.session_state['질문'] != None
#             cond2 = st.session_state['질문'] != ''
#             if cond1 & cond2:
#                 with st.spinner('Wait for it...'):
#                     res = pandas_ai.run(df, prompt=st.session_state['질문'])
#                 st.write(res)
#                 st.write(type(res))
#                 st.pyplot(res)
#             else:
#                 st.warning("질문을 입력해주세요..")


# #############################################
# page_title = '데이터 자동 시각화'
# page_icon = '📊'

# st.set_page_config(page_title=page_title,
#                    layout='wide',
#                    page_icon=page_icon
#                    )

# last_params = {
#     '질문': None,
# }
# elements = last_params.copy()


# llm = OpenAI(api_token=getsecret("openai"))
# pandas_ai = PandasAI(llm)


# #############################################
# # 제목
# st.markdown(f"# {page_title} {page_icon}")
# st.markdown("> 소비자가 열광할 메타 (페이스북, 인스타그램) 광고의 내용을 생성해보세요.")

# #############################################
# # 본문

# # InputLayout
# createInputLayout(elements)
