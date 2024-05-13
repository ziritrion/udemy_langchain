import os

from langchain.prompts.prompt import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_community.chat_models import ChatOllama
from langchain.chains import LLMChain

from third_parties.linkedin import scrape_linkedin_profile

if __name__ == "__main__":
    print("Hello langchain")

    summary_template = """
Given the LinkedIn information {information} about a person, I want you to create:
1. A short summary
2. Two interesting facts about them
    """

    summary_prompt_template = PromptTemplate(
        input_variables=["information"], template=summary_template
    )

    #llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")
    # for localhost
    ollama_model_name = os.environ.get("OLLAMA_MODEL")
    ollama_base_url = os.environ.get("OLLAMA_BASE_URL")
    llm = ChatOllama(model=ollama_model_name, base_url=ollama_base_url)

    chain = LLMChain(llm=llm, prompt=summary_prompt_template)
    linkedin_data = scrape_linkedin_profile(linkedin_profile_url="none", mock=True)
    res = chain.invoke(input={'information': linkedin_data})

    print(res)