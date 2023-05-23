import pandas as pd
import os

from kiwipiepy import Kiwi
from keybert import KeyBERT
from transformers import BertModel

from text_preprocessing import TextPreprocessing
from update_db import Updatae_DB

kiwi = Kiwi()
textpreprocessing = TextPreprocessing()


class KeywordExtracter:
    def __init__(self) -> None:
        self.kw_model = None
        self._setting()

    def _setting(self):
        model = BertModel.from_pretrained('skt/kobert-base-v1')
        self.kw_model = KeyBERT(model)

    def run(self):
        pass

    def extract_keyword(self, text, top_n: int = 20):
        text = textpreprocessing.preprocssing(text)
        text = self._noun_extractor(text)
        text = self._keybert(text, top_n)
        return text

    # 명사 추출 함수
    def _noun_extractor(self, text):
        results = []
        result = kiwi.analyze(text)
        for token, pos, _, _ in result[0][0]:
            if len(token) != 1 and pos.startswith('N') or pos.startswith('SL'):
                results.append(token)
        return ' '.join(results)

    def _keybert(self, text, top_n):
        keywords = self.kw_model.extract_keywords(
            text, keyphrase_ngram_range=(1, 1), stop_words=None, top_n=top_n)
        keywords = list(map(lambda x: x[0], keywords))
        return keywords


if __name__ == '__main__':
    file_path = 'last/data/Data_Reviews.csv'
    # db_path = "last/data/ver_0520.db"
    # print(os.getcwd())
    df = pd.read_csv(file_path, sep='\t')

    # db = Updatae_DB(db_path=db_path)

    # print(df)
    keyword_extracter = KeywordExtracter()
    df['data'] = df['data'].apply(keyword_extracter.extract_keyword)
    print(df['search_id'])
