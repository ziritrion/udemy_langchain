import os

from langchain.prompts.prompt import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_community.chat_models import ChatOllama
from langchain_openai import AzureChatOpenAI
#from langchain.chains import LLMChain

from third_parties.linkedin import scrape_linkedin_profile
from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent

from output_parsers import summary_parser

def ice_break_with(name: str) -> str:
    linkedin_url = linkedin_lookup_agent(name=name)
    linkedin_data = scrape_linkedin_profile(linkedin_profile_url=linkedin_url, mock=True)

    summary_template = """
Given the LinkedIn information {information} about a person, I want you to create:
1. A short summary
2. Two interesting facts about them
\n{format_instructions}
    """
    summary_prompt_template = PromptTemplate(
        input_variables=["information"],
        template=summary_template,
        partial_variables={"format_instructions": summary_parser.get_format_instructions()},
    )

    # OPENAI
    #llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")

    # OLLAMA
    #ollama_model_name = os.environ.get("OLLAMA_MODEL")
    #ollama_base_url = os.environ.get("OLLAMA_BASE_URL")
    #llm = ChatOllama(model=ollama_model_name, base_url=ollama_base_url)

    # AZURE OPENAI
    llm = AzureChatOpenAI(
        azure_deployment=os.environ.get('DEPLOYMENT_NAME'),
        temperature=0,
    )

    #chain = LLMChain(llm=llm, prompt=summary_prompt_template) # DEPRECATED
    chain = summary_prompt_template | llm | summary_parser
    res = chain.invoke(input={'information': linkedin_data})
    print(res)

if __name__ == "__main__":
    print("Ice Breaker")
    ice_break_with(name="Alvaro Navas Peire data scientist minsait LinkedIn")
    