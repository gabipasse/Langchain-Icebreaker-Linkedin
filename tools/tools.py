from langchain_community.tools.tavily_search import TavilySearchResults


def get_profile_url_tavily(name: str) -> list[dict[str, str]]:
    """Searches for Linkedin or Twitter Profile Page.

    Parameters
    ----------
    name: str
        Name of the person for which the information will be crawled from the internet.

    Return
    ------
    list[dict[str, str]]
        List containg the information scrapped for the provided name.
    """

    search = TavilySearchResults()
    res = search.run(f"{name}")

    return res
