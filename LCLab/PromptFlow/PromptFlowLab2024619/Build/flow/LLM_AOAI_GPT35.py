
from promptflow import tool
import os
from langchain_openai import AzureOpenAI

os.environ["OPENAI_API_VERSION"] = "2023-12-01-preview"
os.environ["AZURE_OPENAI_ENDPOINT"] = "https://aoaius.openai.azure.com/"
os.environ["AZURE_OPENAI_API_KEY"] = "f27f3aee0a9d46ebbd89e0d95bd07345"


# The inputs section will change based on the arguments of the tool function, after you save the code
# Adding type to arguments and return value will help the system show the types properly
# Please update the function name/signature per need
@tool
def my_python_tool(input1: str) -> str:
    
    llm = AzureOpenAI(
        deployment_name="gpt35ti",
    )
    response = llm.invoke(input1)
    print('\n\ninput\n' + input1 + 'response\n\n' + response)
    return response
