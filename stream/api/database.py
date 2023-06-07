import streamlit as st

import time
import numpy as np
import pandas as pd

# conn = st.experimental_connection('pets_db', type='sql')


def insert_row_in_csv(csv_file, row_dict):
    # CSV 파일 불러오기
    data = pd.read_csv(csv_file)

    # 행 값 추가
    data = data.append(row_dict, ignore_index=True)
    data = data.replace({np.nan: None})

    # 수정된 데이터 저장
    data.to_csv(csv_file, index=False)


def update_in_csv(df, path):
    df = df.replace({np.nan: None})
    df.to_csv(path, index=False)


# pet_owners = conn.query('select * from pet_owners')
# st.dataframe(pet_owners)
