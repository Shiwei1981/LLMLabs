
from promptflow import tool
import os
from langchain_openai import AzureOpenAI
from langchain_core.messages import HumanMessage
from langchain_openai import AzureChatOpenAI

os.environ["OPENAI_API_VERSION"] = "2023-12-01-preview"
os.environ["AZURE_OPENAI_ENDPOINT"] = "https://aoaincussw.openai.azure.com/"
os.environ["AZURE_OPENAI_API_KEY"] = "075862edf906471abb2ad0d78140342b"


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
        openai_api_version="2023-12-01-preview",
        azure_deployment="gpt4o",
        azure_endpoint="https://aoaincussw.openai.azure.com/",
        api_key="075862edf906471abb2ad0d78140342b",
        max_tokens=4096,
        temperature=0.9,
    )
    message = HumanMessage(
        content=input1
    )

    response = model.invoke([message])


    return response.content
