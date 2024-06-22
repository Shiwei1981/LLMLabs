# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

from promptflow.core import tool

# The inputs section will change based on the arguments of the tool function, after you save the code
# Adding type to arguments and return value will help the system show the types properly
# Please update the function name/signature per need
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_models import ChatOllama
from langchain import PromptTemplate, OpenAI



@tool
def my_python_tool(input1: str, input2: str) -> str:
    prompt = ChatPromptTemplate.from_messages([("system", input1), ("human", "{input}")])

    model= ChatOllama(model='llama3')

    chain = prompt | model | StrOutputParser()
    response = chain.invoke({"input":input2})
    print(response)
    return "Prompt: " + input2 + "Output: " + response
