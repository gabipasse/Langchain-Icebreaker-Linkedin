import sys
from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import Tool
from langchain.agents import create_react_agent, AgentExecutor
from langchain import hub
from pathlib import Path


sys.path.append(str(Path(__file__).parent.parent))
from tools.tools import get_profile_url_tavily


def linkedin_lookup_agent(name: str) -> str:
    """Fetch a linkedin profile url using an agent as executor by passing a persons name.

    Parameters
    ----------
    name: str
        Name of the person for which the linkedin profile url will be fetched.

    Return
    ------
    str
        The linkedin url profile.
    """
    llm = ChatOllama(model="llama3")
    template = """given the full name {name_of_person}, i want you to get me a link to their Linkedin profile page.
            Your answer should contain only a URL. Do not complement your answer with anything besides the URL."""

    prompt_template = PromptTemplate(
        template=template, input_variables=["name_of_person"]
    )
    tools_for_agent = [
        Tool(
            name="Crawl Google 4 Linkedin profile page",
            func=get_profile_url_tavily,
            description="Useful for when you need to get the Linkedin page URL",
        )
    ]

    react_prompt = hub.pull("hwchase17/react")
    agent = create_react_agent(llm, tools_for_agent, react_prompt)
    agent_executor = AgentExecutor(
        agent=agent, tools=tools_for_agent, verbose=True, handle_parsing_errors=True
    )

    result = agent_executor.invoke(
        input={"input": prompt_template.format_prompt(name_of_person=name)}
    )

    linkedin_profile_url = result["output"]

    return linkedin_profile_url
