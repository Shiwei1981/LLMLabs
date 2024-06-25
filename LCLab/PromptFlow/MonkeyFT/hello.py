
from promptflow import tool
import os
from langchain_openai import AzureOpenAI
from langchain_core.messages import HumanMessage
from langchain_openai import AzureChatOpenAI


# The inputs section will change based on the arguments of the tool function, after you save the code
# Adding type to arguments and return value will help the system show the types properly
# Please update the function name/signature per need
@tool
def my_python_tool(input1: str) -> str:
    
    '''
    llm = AzureOpenAI(
        deployment_name="gpt4",
    )
    response = llm.invoke(input1)
    print('\n\ninput：\n' + input1 + 'response：\n\n' + response)
    '''
    model = AzureChatOpenAI(
        azure_deployment="GPT4",
        max_tokens=4096,
        temperature=0.9,
    )
    message = HumanMessage(
        content=input1
    )

    response = model.invoke([message])


    return response.content
