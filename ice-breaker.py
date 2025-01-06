from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from third_parties.linkedin import scrape_linkedin_profile
from agents.linkedin_lookup_agent import linkedin_lookup_agent


def ice_break_with(name: str) -> str:
    """Summarize information, fetched from a persons linkedin profile, to be used as ice break for future interactions.

    Parameters
    ----------
    name: str
        Name of the person for which the ice breaking information will be organized.

    Return
    ------
    str
        The ice break information for the required name.
    """
    linkedin_url = linkedin_lookup_agent(name=name)
    linkedin_data = scrape_linkedin_profile(linkedin_profile_url=linkedin_url)

    summary_template = """Given the Linkedin information {information} about a person. I want you to create:
    1. A short summary
    2. Two interesting facts about them"""

    summary_prompt_template = PromptTemplate(
        input_variables=["information"], template=summary_template
    )

    llm = ChatOllama(model="llama3")
    chain = summary_prompt_template | llm | StrOutputParser()

    result = chain.invoke(input={"information": linkedin_data})

    print("linkedin_url:", linkedin_url)

    return result


def main():
    load_dotenv()

    ice_break_information = ice_break_with(name="Eden Marco")
    print(ice_break_information)


if __name__ == "__main__":
    main()
