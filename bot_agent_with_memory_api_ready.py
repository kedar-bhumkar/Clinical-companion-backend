from datetime import date
from typing import Any, Dict
from langchain_openai import ChatOpenAI
from langchain.agents import tool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents.format_scratchpad.openai_tools import (
    format_to_openai_tool_messages,
)
from langchain_core.messages import AIMessage, HumanMessage
from langchain.agents.output_parsers.openai_tools import OpenAIToolsAgentOutputParser
from langchain.agents import AgentExecutor

#from mock_patient_data import *
from mock_data import *
import os



MEMORY_KEY = "chat_history"
cache ={}

def chat( system_prompt, user_input, functions, model):
    chat_history = []
    
    os.environ["OPENAI_API_KEY"] = shared_data_instance.get_data('key')

  
    llm = ChatOpenAI(model=model, temperature=0)
    tools = [globals()[name] for name in functions if name in globals()]


    print("tools", tools)

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                system_prompt,
            ),
            MessagesPlaceholder(variable_name=MEMORY_KEY),        
            ("user", "Question from the user : {input}."),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ]
    )

    llm_with_tools = llm.bind_tools(tools)


    agent = (
        {
            "input": lambda x: x["input"],
            "agent_scratchpad": lambda x: format_to_openai_tool_messages(
                x["intermediate_steps"]
            ),
        "chat_history": lambda x: x["chat_history"],

        }
        | prompt
        | llm_with_tools
        | OpenAIToolsAgentOutputParser()
    )

    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    result = agent_executor.invoke({"input": "User Question-" + user_input, "chat_history": chat_history})
    chat_history.extend(
        [
            HumanMessage(content=user_input),
            AIMessage(content=result["output"]),
        ]
    )        

    return result['output']