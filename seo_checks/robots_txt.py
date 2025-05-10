import requests
from urllib.parse import urlparse

def check_robots_txt(url):
    try:
        parsed_url = urlparse(url)
        base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
        robots_url = f"{base_url}/robots.txt"

        response = requests.get(robots_url, headers={'User-Agent': 'Mozilla/5.0'})
        
        if response.status_code == 200:
            content = response.text
            is_disallowed = "Disallow: /" in content
            return {
                "robots_txt_found": True,
                "disallow_all": is_disallowed,
                "robots_txt_url": robots_url
            }
        else:
            return {
                "robots_txt_found": False,
                "disallow_all": None,
                "robots_txt_url": robots_url
            }

    except Exception as e:
        return {
            "robots_txt_found": False,
            "disallow_all": None,
            "error": str(e)
        }
