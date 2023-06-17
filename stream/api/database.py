import streamlit as st

import time
import numpy as np
import pandas as pd

import os
import requests

# conn = st.experimental_connection('pets_db', type='sql')


def makeCSV(filename, cols):
    df = pd.DataFrame(columns=cols)
    df.to_csv(filename, index=False)


def initCSV(dbDict):
    dirList = os.listdir(os.getcwd())
    for filename, cols in dbDict.items():
        if filename not in dirList:
            makeCSV(filename, cols)


def insert_row_in_csv(csv_file, row_dict):
    try:
        # CSV 파일 불러오기
        data = pd.read_csv(csv_file)
    except:
        data = pd.read_csv(f'stream/{csv_file}')
    # 행 값 추가
    data = data.append(row_dict, ignore_index=True)
    data = data.replace({np.nan: None})

    # 수정된 데이터 저장
    data.to_csv(csv_file, index=False)


def update_in_csv(df, path):
    df = df.replace({np.nan: None})
    try:
        # CSV 파일 불러오기
        data = pd.read_csv(path)
        df.to_csv(path, index=False)
    except:
        data = pd.read_csv(f'stream/{path}')
        df.to_csv(f'stream/{path}', index=False)


def download_file(url, save_path):
    response = requests.get(url)
    with open(save_path, 'wb') as file:
        file.write(response.content)


def html_loader(html_info):
    try:
        with open(html_info['path'], 'r') as file:
            html_code = file.read()
    except:
        download_file(html_info['url'], html_info['path'])
        with open(html_info['path'], 'r') as file:
            html_code = file.read()
    return html_code

# pet_owners = conn.query('select * from pet_owners')
# st.dataframe(pet_owners)
