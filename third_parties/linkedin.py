import os
import requests
import joblib
from dotenv import load_dotenv

cache_dir = "linkedin_cache"
os.makedirs(cache_dir, exist_ok=True)
memory = joblib.Memory(cache_dir, verbose=0)

load_dotenv()


@memory.cache
def scrape_linkedin_profile(linkedin_profile_url: str) -> dict[str, str]:
    """Scrape information from Linkedin profiles.
    Mannualy scrape the information from the Linkedin profile.

    Parameters
    ----------
    linkedin_profile_url: str
        Linkedin profile url which will be used to scrape informations from.

    Return
    ------
    dict[str, str]
        Dicionary containing the scrapped information.
    """

    api_key = os.getenv("API_KEY")
    headers = {"Authorization": "Bearer " + api_key}
    api_endpoint = "https://nubela.co/proxycurl/api/v2/linkedin"
    params = {
        "linkedin_profile_url": linkedin_profile_url,
        "extra": "include",
        "github_profile_id": "include",
        "facebook_profile_id": "include",
        "twitter_profile_id": "include",
        "personal_contact_number": "include",
        "personal_email": "include",
        "inferred_salary": "include",
        "skills": "include",
        "use_cache": "if-present",
        "fallback_to_cache": "on-error",
    }
    response = requests.get(api_endpoint, params=params, headers=headers)

    data = response.json()

    data = {
        k: v
        for k, v in data.items()
        if v not in ([], "", "", None)
        and k not in ["people_also_viewed", "certifications"]
    }

    if data.get("groups"):
        for group_dict in data.get("groups"):
            group_dict.pop("profile_pic_url")

    return data
