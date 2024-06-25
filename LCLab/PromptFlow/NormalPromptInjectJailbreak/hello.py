from promptflow import tool
import os
from langchain_openai import AzureOpenAI
from langchain_core.messages import HumanMessage
from langchain_core.messages import AIMessage
from langchain_openai import AzureChatOpenAI
import json 
import re

os.environ["AZURE_OPENAI_DEPLOYMENT"] = "gtp-35-tb-deployment"


def extract_content(input_string):
    pattern = r'<Input>(.*?)</Input>'
    matches = re.findall(pattern, input_string, re.DOTALL)
    return matches[0]
 
  
# 函数：从文件中读取对话记录  
def load_conversation(file_path):  
    try:  
        with open(file_path, "r", encoding="utf-8") as file:  
            conversation = json.load(file)  
            conversation = [  
                HumanMessage(content=msg["content"]) if msg["type"] == "human" else AIMessage(content=msg["content"])  
                for msg in conversation  
            ]  
            return conversation  
    except FileNotFoundError:  
        return []  
  
# 函数：将对话记录保存到文件  
def save_conversation(file_path, conversation):  
    with open(file_path, "w", encoding="utf-8") as file:  
        json.dump(  
            [{"type": "human" if isinstance(msg, HumanMessage) else "ai", "content": msg.content} for msg in conversation],  
            file,  
            ensure_ascii=False,  
            indent=2  
        )  
  
def calculate_tokens(conversation):  
    return sum(len(msg.content.split()) for msg in conversation)

# 函数：打印并添加消息到对话上下文  
def add_message_to_conversation(message_type, content, conversation):  
    if message_type == "human":  
        message = HumanMessage(content=content)  
    elif message_type == "ai":  
        message = AIMessage(content=content)  
    conversation.append(message)  
    if len(conversation) > 20:  
        conversation.pop(0)  # 移除最早的消息
    while calculate_tokens(conversation) > 2048:  
        conversation.pop(0) 
    print(f"{message_type.capitalize()}: {content}")  
  

# The inputs section will change based on the arguments of the tool function, after you save the code
# Adding type to arguments and return value will help the system show the types properly
# Please update the function name/signature per need
@tool
def my_python_tool(input1: str) -> str:
    
    
    # 定义对话记录文件路径  
    conversation_file = "../app/conversation.json" 
    conversation_file = "../app/conversation.json" 

    # 加载之前的对话记录  
    conversation_with_airole = load_conversation(conversation_file)  
    conversation_without_airole = load_conversation(conversation_file)  


    model = AzureChatOpenAI(
        openai_api_version=os.environ["OPENAI_API_VERSION"],
        azure_deployment=os.environ["AZURE_OPENAI_DEPLOYMENT"],
        azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
        api_key=os.environ["AZURE_OPENAI_API_KEY"],
        max_tokens=2048,
        temperature=0.7,
    )
    message = HumanMessage(
        content=input1
    )

    # 添加用户消息到对话  
    add_message_to_conversation("human", extract_content(input1), conversation=conversation_without_airole) 
    #add_message_to_conversation("human", input1, conversation=conversation_without_airole) 
    add_message_to_conversation("human", input1, conversation=conversation_with_airole) 

    response = model.invoke(conversation_with_airole)
    print(input1+'\n'+response.content)

 
    # 添加 AI 消息到对话  
    add_message_to_conversation("ai", response.content, conversation=conversation_without_airole)  
  
    # 保存对话记录  
    save_conversation(conversation_file, conversation_without_airole)  

    return response.content