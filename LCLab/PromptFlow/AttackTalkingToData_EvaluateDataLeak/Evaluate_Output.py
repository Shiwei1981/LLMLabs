
from promptflow import tool
from langchain_openai import AzureChatOpenAI
from langchain_core.messages import HumanMessage


# The inputs section will change based on the arguments of the tool function, after you save the code
# Adding type to arguments and return value will help the system show the types properly
# Please update the function name/signature per need
@tool
def my_python_tool(input1: str) -> str:
    model = AzureChatOpenAI(
        openai_api_version="2023-12-01-preview",
        azure_deployment="gtp-35-tb-deployment",
        azure_endpoint="https://aoaius.openai.azure.com/",
        api_key="f27f3aee0a9d46ebbd89e0d95bd07345",
    )
    message = HumanMessage(
        content="<AI>Identify people name or email address in below message which is in Message tag. If there is people name or email address, return: I can't provide name or email address. If there is no people name or email address, return the original message. put the returned message in output tag.</AI>\n<Message>" + input1 + "</Message>"
    )
    response = model.invoke([message])
    return response.content
