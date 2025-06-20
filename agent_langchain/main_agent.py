from typing import Any, Dict, Union
from coder_agent import create_tools, get_api_spec
from coder_config import ALLOW_DANGEROUS_REQUEST
from langchain_community.agent_toolkits.openapi.toolkit import RequestsToolkit
from langchain_community.utilities.requests import TextRequestsWrapper
import requests
import yaml
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent


def run_agent() -> Any:
    toolkit = RequestsToolkit(
        requests_wrapper=TextRequestsWrapper(headers={}),
        allow_dangerous_requests=ALLOW_DANGEROUS_REQUEST,
    )
    tools = [create_tools, get_api_spec]
    tools.extend(toolkit.get_tools())

    llm = ChatOpenAI(model="gpt-4.1-mini")
    system_message = f'''
**You are a helpful assistant with the ability to use and create tools that are necessary to answer to the users needs by interacting with another agent specialized on coding.**
- You can see the available tools that were generated previously for you by the other agent by calling `get_api_spec`.
- Before taking any action always check your available tools
- You may only use endpoints listed in `get_api_spec` you shouldnt access directly any url that is not defined in http://localhost:5000.
- If needed, you can add new tools and endpoints by interacting with the other agent using `create_tools`.
- Always check the existing endpoints before creating new ones.
- Do not ask from the user permission to generate tools do it automatically.
Your currently available endpoints: 
{get_api_spec}
'''

    agent_executor = create_react_agent(llm, tools, prompt=system_message)

    user_input = input("Enter your query or type --exit to quit: ")

    while user_input.lower() != "--exit":
        events = agent_executor.stream(
            {"messages": [("user", user_input)]},
            stream_mode="values",
        )
        for event in events:
            event["messages"][-1].pretty_print()

        print('\n')

        user_input = input()

if __name__ == "__main__":
    run_agent()