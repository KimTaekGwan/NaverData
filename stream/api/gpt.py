import re
from langchain.callbacks import get_openai_callback
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain import PromptTemplate, LLMChain
from langchain.chat_models import ChatOpenAI
import os
from dotenv import load_dotenv

import os
import sys
import urllib.request
import requests

import streamlit as st


def getsecret(name):
    res = os.getenv(name)
    if res == None:
        return st.secrets[name]
    return res


class Translater:
    def __init__(self):
        self.setting()
        self.client_id = getsecret("naver_client_id")
        self.client_secret = getsecret("naver_client_secret")
        print(self.client_id)

    def setting(self):
        load_dotenv()

    def en2ko(self, text):
        encText = urllib.parse.quote(text)
        data = "source=en&target=ko&text=" + encText
        url = "https://naveropenapi.apigw.ntruss.com/nmt/v1/translation"
        request = urllib.request.Request(url)
        request.add_header("X-NCP-APIGW-API-KEY-ID", self.client_id)
        request.add_header("X-NCP-APIGW-API-KEY", self.client_secret)
        response = urllib.request.urlopen(request, data=data.encode("utf-8"))
        # response = urllib.request.urlopen(request, data=data)
        rescode = response.getcode()
        if (rescode == 200):
            response_body = response.read()
            print(response_body.decode('utf-8'))
            return response_body.decode('utf-8')
        else:
            print("Error Code:" + rescode)
            return rescode


class CopyWriter:
    def __init__(self):
        self.setting()
        self.translater = Translater()

    def setting(self):
        load_dotenv()

    def set_chain(self, temperature: int = 0.5):
        chat = ChatOpenAI(
            temperature=temperature,
            # max_tokens=,
            # model_name='text-davinci-003',
            openai_api_key=getsecret("openai")
        )
        system_message_prompt = SystemMessagePromptTemplate(
            prompt=PromptTemplate(
                template="You are an assistant who helps me copywrite \
                    to find advertisement copy using the condition given to me.",
                input_variables=[]
            )
        )
        human_message_prompt = HumanMessagePromptTemplate(
            prompt=PromptTemplate(
                template="{res_prompt}",
                input_variables=["res_prompt"]
            )
        )
        chat_prompt = ChatPromptTemplate.from_messages(
            [system_message_prompt, human_message_prompt]
        )
        self.chain = LLMChain(llm=chat, prompt=chat_prompt)

    def prompt_text(self, product: str, description: str, keywords: list, num_copy: int) -> str:
        keywords = ', '.join(set([word for word in keywords if word]))
        prompt = f"""
        I am creating social media posts with the goal of selling my \
        {product} and driving people to my product page. \
        I suggest seven social media posts that capitalize on the various benefits of \
        {product} that you can use to drive traffic to my product page.
        Convince potential customers who are reading your social media posts to buy \
        {product}.
        Speak directly to the customer so they know the exact benefits they will receive.
        \nProduct description: {description}
        \nInclude keywords : {keywords}\n"""
        prompt += "\nOutput:"
        for num in range(1, num_copy+1):
            prompt += f'\n{num}. '
        return prompt

    def process_run(self, product: str, description: str, keywords: list, num_copy: int):
        self.set_chain()
        res_prompt = self.prompt_text(
            product, description, keywords, num_copy)
        with get_openai_callback() as cb:
            res = self.chain.run(res_prompt=res_prompt)
            res = self.translater.en2ko(res)
            topics = re.findall(r"\d+\.\s(.+)", res)
            # print(cb)
            res_tokens = cb.total_tokens
            # print(res_tokens)
        topics = re.findall(r"\d+\.\s(.+)", res)
        return topics
        # return {'status': True,
        #         'msg': 'Brainstoming Idea',
        #         'data': topics,
        #         'total_tokens': res_tokens}


class Brainstoming:
    def __init__(self):
        self.setting()

    def setting(self):
        load_dotenv()

    def set_chain(self, temperature: int = 0.5):
        chat = ChatOpenAI(
            temperature=temperature,
            # max_tokens=,
            # model_name='text-davinci-003',
            openai_api_key=getsecret("openai")
        )
        system_message_prompt = SystemMessagePromptTemplate(
            prompt=PromptTemplate(
                template="You are an assistant who helps me brainstorm \
                          to find creative topics using the data given to me.",
                input_variables=[]
            )
        )
        human_message_prompt = HumanMessagePromptTemplate(
            prompt=PromptTemplate(
                template="{res_prompt}",
                input_variables=["res_prompt"]
            )
        )
        chat_prompt = ChatPromptTemplate.from_messages(
            [system_message_prompt, human_message_prompt]
        )
        self.chain = LLMChain(llm=chat, prompt=chat_prompt)

    def prompt_text(self, data_prompt: str, field: str, purpose: str, num_topics: int) -> str:
        prompt = f"Generate {num_topics} topics in the {field} field for the following purpose: {purpose}\n\nData:\n"
        prompt += data_prompt
        prompt += "\nOutput:"
        for num in range(1, num_topics+1):
            prompt += f'\n{num}. '
        return prompt

    def generate_prompt(self, data_infos=dict) -> str:
        """
        데이터 정보가 담긴 dict를 받아서 해당 데이터에 대한 프롬프트를 생성합니다.

        Args:
            data_infos (dict): data info(dict)가 담긴 dict
                각 데이터의 id값을 key로 가지고 있습니다.
            data_info (dict): 데이터 정보가 담긴 dict
                - 'data_name' (str): 데이터명
                - 'data_description' (str): 데이터 설명
                - 'columns' (list of dict): 데이터 칼럼 정보가 담긴 dict의 리스트
                    - 'column_name' (str): 칼럼명
                    - 'column_description' (str): 칼럼 설명

        Returns:
            str: 해당 데이터에 대한 프롬프트 문자열입니다.
        """
        prompt = ""
        for n, (_, data) in enumerate(data_infos.items(), start=1):
            prompt += f"{n}. {data['data_name']}\n"
            prompt += f"- data description\n"
            prompt += f"{data['data_description']}\n"
            prompt += f"- columns info\n"
            for column in data['columns']:
                prompt += f"\t- {column['column_name']}: {column['column_description']}\n"
        return prompt

    def process_run(self, data_infos, field: str, purpose: str, num_topics: int):
        self.set_chain()
        data_prompt = self.generate_prompt(data_infos)
        res_prompt = self.prompt_text(data_prompt, field, purpose, num_topics)

        with get_openai_callback() as cb:
            res = self.chain.run(res_prompt=res_prompt)
            topics = re.findall(r"\d+\.\s(.+)", res)
            # print(cb)
            res_tokens = cb.total_tokens
            # print(res_tokens)
        topics = re.findall(r"\d+\.\s(.+)", res)
        return {'status': True,
                'msg': 'Brainstoming Idea',
                'data': topics,
                'total_tokens': res_tokens}


if __name__ == '__main__':
    trans = Translater()
    print(trans.en2ko('hihihihihihihih'))
