from langchain.agents import tool
from typing import Optional

# Note: Tools are now defined within the Chatbot class
# This file can be used for additional shared tools if needed

@tool
def example_utility_tool(query: str) -> str:
    """Example of an additional tool that could be used"""
    return "This is an example tool response"