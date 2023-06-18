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
            return eval(response_body.decode('utf-8'))['message']['result']['translatedText']
        else:
            print("Error Code:" + rescode)
            return rescode


class CopyWriter:
    def __init__(self, page_num):
        self.setting()
        self.translater = Translater()
        self.page_num = page_num

    def setting(self):
        load_dotenv()

    def set_chain(self, temperature: int = 0.5):
        chat = ChatOpenAI(
            temperature=temperature,
            max_tokens=3500,
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

    def prompt_text(self, params: dict) -> str:
        # prompt = """내 제품을 판매하고 사람들을 내 제품 페이지로 유도하는 것을 목표로 소셜 미디어 게시물을 작성하고 있습니다. \
        # 내 제품 페이지로 트래픽을 유도하는 데 사용할 수 있는 제품의 다양한 이점을 활용하는 소셜 미디어 게시물을 제안합니다. \
        # 소셜 미디어 게시물을 읽고 있는 잠재 고객이 제품을 구매하도록 설득하세요. 고객이 받게 될 정확한 혜택을 알 수 있도록 고객에게 직접 이야기하세요. \
        # 아래 제품에 대한 정보와 나의 요구사항을 보고 소셜 미디어 게시물에서 사용할 최종 문구를 한국어 알려줘."""

        #
        # prompt = """내 제품을 판매하고 사람들을 내 제품 페이지로 유도하는 것을 목표로 앱 알림 메시지를 작성하고 있습니다. \
        # 앱으로 트래픽을 유도하는 데 사용할 수 있는 앱 알림 메시지을 제안합니다. \
        # 앱 알림 메시지을 읽고 있는 고객이 앱에 들어오고, 제품을 구매하도록 설득하세요. 고객이 받게 될 정확한 혜택을 알 수 있도록 고객에게 직접 이야기하세요. \
        # 아래 나의 요구사항을 보고 앱 알림 메시지에서 사용할 최종 문구를 한국어 알려줘.

        # 1. SNS 광고문구
        if self.page_num == 1:
            prompt = """I am creating a social media post with the goal of selling my product and driving people \
            to my product page. I suggest a social media post that leverages the various benefits of my \
            product that can be used to drive traffic to my product page. Convince potential customers who \
            are reading your social media post to purchase your product. Talk directly to your customers so \
            that they know the exact benefits they will receive. Look at the information about the product below \
            and my requirements and tell me the final wording to use in the social media post."""

        elif self.page_num == 2:
            prompt = """I am creating an SMS promotional message with the goal of selling my product and driving people to my product page.\
            Convince customers who are reading your SMS promotion message to buy your product. \
            Speak directly to them so that they know about the promotion you are running and the exact benefits they will receive. \
            Take a look at my requirements below and tell me in English the final wording to use in the SMS promotion message."""

        elif self.page_num == 3:
            prompt = """I'm creating an app notification message with the goal of selling my product \
            and driving people to my product page. Suggest an app notification message \
            that I can use to drive traffic to my app. \
            Convince customers who are reading your app notification message to enter your app and buy your product. \
            Talk directly to your customers so they know the exact benefits they will receive.\ 
            Look at my requirements below and tell me in English the final wording to use in the app notification message."""

        for key, value in params.items():
            if isinstance(value, list) or isinstance(value, set):
                res_value = ', '.join(
                    set([word for word in value.split() if word]))
            else:
                res_value = value
            prompt += f'\n{key} : {res_value}'
        # prompt += "\n최종 한국어 문구 결과물:"
        prompt += "\nOutput:"
        for num in range(1, params['생성 문구 수']+1):
            prompt += f'\n{num}. '
        return prompt

    def process_run(self, params: dict):
        self.set_chain()
        res_prompt = self.prompt_text(params)
        with get_openai_callback() as cb:
            res = self.chain.run(res_prompt=res_prompt)
            topics = re.findall(r"\d+\.\s(.+)", res)
            res_tokens = cb.total_tokens
        res = re.findall(r"\d+\.\s(.+)", res)
        # return {'data': res,
        #         'total_tokens': res_tokens}
        res = [self.translater.en2ko(topic)
               for topic in topics]
        return {'data': res,
                'total_tokens': res_tokens}


if __name__ == '__main__':
    trans = Translater()
    print(trans.en2ko('hihihihihihihih'))
