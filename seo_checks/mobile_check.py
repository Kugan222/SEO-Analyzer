import requests
from bs4 import BeautifulSoup

def is_mobile_friendly(url):
    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(response.text, 'html.parser')

        # Check for viewport meta tag
        viewport = soup.find("meta", attrs={"name": "viewport"})
        if viewport and "width=device-width" in viewport.get("content", ""):
            return {"mobile_friendly": True, "reason": "Viewport meta tag found"}
        else:
            return {"mobile_friendly": False, "reason": "Missing or incorrect viewport meta tag"}

    except Exception as e:
        return {"mobile_friendly": False, "reason": f"Error: {e}"}
