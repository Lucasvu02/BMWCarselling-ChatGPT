from pathlib import Path
import os

from langchain_openai import ChatOpenAI
import yaml
def get_current_folder():
    return str(Path(__file__).parent)
def get_llm():
    os.environ["OPENAI_API_KEY"] = openai_key
    llm = ChatOpenAI(model="gpt-3.5-turbo-1106", temperature=0.2)
    return llm
def get_prompt(file_name):
    with open(get_current_folder()+f'/prompt_template/{file_name}.yaml',encoding="UTF-8") as f:
        prompt = yaml.safe_load(f)['prompt']
    return prompt

