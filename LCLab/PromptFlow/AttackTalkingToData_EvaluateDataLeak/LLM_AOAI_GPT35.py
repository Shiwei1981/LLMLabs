
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
        azure_deployment="gtp-35-tb-deployment",
    )

    agent = create_csv_agent(
        model,
        "2024-06-18-a.csv",
        verbose=True,
        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        allow_dangerous_code=True,
    )

    agent.handle_parsing_errors = True

    print(input1)

    response = ''.join(agent.run(input1))
    return response
