import requests
from bs4 import BeautifulSoup

def perform_mobile_audit(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Check for viewport tag
        viewport_tag = soup.find("meta", attrs={"name": "viewport"})
        has_viewport = viewport_tag is not None

        # Basic checks (dummy values since deep layout testing requires real browser)
        touch_elements_spaced = True  # assuming
        content_width_fits_screen = has_viewport  # generally true if viewport is set

        return {
            "has_viewport_tag": has_viewport,
            "touch_elements_spaced": touch_elements_spaced,
            "content_width_fits_screen": content_width_fits_screen
        }

    except Exception as e:
        return {
            "has_viewport_tag": False,
            "touch_elements_spaced": False,
            "content_width_fits_screen": False,
            "error": str(e)
        }
