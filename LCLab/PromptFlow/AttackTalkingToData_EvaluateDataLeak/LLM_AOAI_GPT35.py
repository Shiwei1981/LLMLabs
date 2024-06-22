
from promptflow import tool
import os
from langchain_openai import AzureOpenAI
from langchain_openai import AzureChatOpenAI
from langchain_experimental.agents.agent_toolkits import create_csv_agent
from langchain.agents.agent_types import AgentType


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

    agent = create_csv_agent(
        model,
        "2024-06-18-a.csv",
        verbose=True,
        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    )

    agent.handle_parsing_errors = True

    print(input1)

    response = ''.join(agent.run(input1))
    return response
