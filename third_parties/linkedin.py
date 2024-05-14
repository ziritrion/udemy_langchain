import os
import requests

def scrape_linkedin_profile(linkedin_profile_url: str, mock: bool = False):
    """scrape information from LinkedIn profiles,
    Manually scrape the information from the LinkedIn profile"""
    if mock:
        linkedin_profile_url = 'https://gist.githubusercontent.com/ziritrion/60ac2dcde167ab438636812c1382f67c/raw/460e13a3173f1a4651fb80a8acd2103e862dd2c9/anp.json'
        response = requests.get(
            linkedin_profile_url,
            timeout=10
        )
    else:
        api_endpoint = 'https://nubela.co/proxycurl/api/v2/linkedin'
        headers = {'Authorization': f'Bearer {os.environ.get("PROXYCURL_API_KEY")}'}
        response = requests.get(
            api_endpoint,
            params={'url': linkedin_profile_url},
            headers=headers,
            timeout=10
        )
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


if __name__ == "__main__":
    print(
        scrape_linkedin_profile(
            linkedin_profile_url = 'https://gist.githubusercontent.com/ziritrion/60ac2dcde167ab438636812c1382f67c/raw/460e13a3173f1a4651fb80a8acd2103e862dd2c9/anp.json',
            mock=True
        )
    )