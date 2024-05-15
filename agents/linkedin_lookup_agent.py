import os
from langchain_openai import ChatOpenAI
from langchain_openai import AzureChatOpenAI
from langchain_community.chat_models import ChatOllama
from langchain.prompts.prompt import PromptTemplate
from langchain_core.tools import Tool
from langchain.agents import (
    create_react_agent,
    AgentExecutor,
)
from langchain import hub

from tools.tools import get_profile_url_tavily

def lookup(name: str) -> str:
    # OLLAMA
    '''
    ollama_model_name = os.environ.get("OLLAMA_MODEL")
    ollama_base_url = os.environ.get("OLLAMA_BASE_URL")
    llm = ChatOllama(model=ollama_model_name, base_url=ollama_base_url)
    '''

    # OPENAI
    '''
    llm = ChatOpenAI(
        temperature=0,
        model="gpt-3.5-turbo",
    )
    '''

    # AZURE OPENAI
    llm = AzureChatOpenAI(
        azure_deployment=os.environ.get('DEPLOYMENT_NAME'),
        temperature=0,
    )


    template  = """Given the full name {name_of_person} I want you to get me a link to their LinkedIn profile page.
                        Your answer should contain only a URL"""
    
    prompt_template = PromptTemplate(
        template=template,
        input_variables=["name_of_person"]
    )

    tools_for_agent = [
        Tool(
            name="Crawl Google 4 linkedin profile page",
            func=get_profile_url_tavily,
            description="useful for when you need to get the LinkedIn Page URL",
        )
    ]

    react_prompt = hub.pull("hwchase17/react") # reasoning engine
    agent = create_react_agent(llm=llm, tools=tools_for_agent, prompt=react_prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools_for_agent, verbose=True)

    result = agent_executor.invoke(
        input={"input": prompt_template.format_prompt(name_of_person=name)}
    )

    linkedin_profile_url = result["output"]
    return linkedin_profile_url

    #return "https://www.linkedin.com/in/alvaronavas/"

if __name__  == "__main__":
    linkedin_url  = lookup(name="Alvaro Navas Peire data scientist minsait LinkedIn")
    print(linkedin_url)