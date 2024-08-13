import json
import argparse
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from src.chatbot.utils import merge_chat_history,merge_document
from src import utils
from src.retrieval.utils import get_retrieval
from langchain_core.prompts import PromptTemplate

retrieval = get_retrieval()
from langchain_community.tools import DuckDuckGoSearchRun

search = DuckDuckGoSearchRun()
api_key = "x"
llm = ChatOpenAI(model="gpt-3.5-turbo-1106", temperature=0.2,api_key = api_key)
def follow_up_chain(api_key):
    follow_up_prompt = utils.get_prompt("follow_up_question")
    follow_up_prompt = PromptTemplate.from_template(follow_up_prompt)
    output_parser = StrOutputParser()
    chain = follow_up_prompt | llm | output_parser
    return chain
def get_follow_up(question,chat_history):
    chain = follow_up_chain()
    query = chain.invoke({"question":question,"chat_history":merge_chat_history(chat_history)})
    query = json.loads(query.replace("\n","").strip().replace("\\",""))
    return query['question']
def input_chain():
    input_handle_prompt = utils.get_prompt("input_guardrail")
    input_handle_prompt = PromptTemplate.from_template(input_handle_prompt)
    output_parser = StrOutputParser()
    chain = input_handle_prompt | llm | output_parser
    return chain
def get_input_handle(question):
    chain = input_chain()
    return chain.invoke({"query":question})
def output_chain():
    prompt = utils.get_prompt("output_guardrail")
    prompt = PromptTemplate.from_template(prompt)
    output_parser = StrOutputParser()
    chain = prompt | llm | output_parser
    return chain
def get_output_handle(question,response):
    chain = output_chain()
    result = chain.invoke({"query":question,"response":response})
    print(result)
    if "NOT OK" in result:
        return False
    return True
def answer_with_rag(question,chat_history):
    prompt = utils.get_prompt("rag")
    prompt = PromptTemplate.from_template(prompt)
    output_parser = StrOutputParser()
    chain = prompt | llm | output_parser
    input_handle = get_input_handle(question)
    if input_handle != "OK":
        return input_handle,"OK"
    follow_up_question = get_follow_up(question,chat_history)
    documents = retrieval.invoke(follow_up_question)
    context = merge_document(documents)
    answer = chain.invoke({"question":question,"chat_history":merge_chat_history(chat_history),"context":context})
    output_check = get_output_handle(question=question,response = answer)
    if output_check != True:
        context = search.invoke(follow_up_question)
        answer = chain.invoke({"question":question,"chat_history":merge_chat_history(chat_history),"context":context})
        chat_history.extend([{"Human":question,"Assistant":answer}])
    return answer,output_check


