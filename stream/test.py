# import pandas as pd
# import os


# def makeCSV(filename, cols):
#     df = pd.DataFrame(columns=cols)
#     df.to_csv(filename, index=False)


# filename = 'hi.csv'
# cols = ['제품 이름', '제품 정보', '필수 키워드',
#         '옵션 키워드', '추가 요구사항', '생성 문구 수']

# dirList = os.listdir(os.getcwd())
# if filename not in dirList:
#     makeCSV(filename, cols)
