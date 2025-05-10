import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

SOCIAL_PLATFORMS = ['facebook.com', 'twitter.com', 'instagram.com', 'linkedin.com', 'youtube.com']

def check_social_links(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')

        social_links = {}
        for link in soup.find_all('a', href=True):
            href = link['href']
            for platform in SOCIAL_PLATFORMS:
                if platform in href:
                    social_links[platform] = href

        return {
            "social_links_found": bool(social_links),
            "links": social_links
        }

    except Exception as e:
        return {
            "social_links_found": False,
            "links": {},
            "error": str(e)
        }
