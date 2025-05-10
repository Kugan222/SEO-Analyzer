import requests
from bs4 import BeautifulSoup

def check_keyword_placement(url, keyword):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        keyword = keyword.lower()

        title = soup.title.string if soup.title else ""
        headings = soup.find_all(['h1', 'h2', 'h3'])
        paragraphs = soup.find_all('p')

        keyword_in_title = keyword in title.lower()
        keyword_in_headings = any(keyword in h.get_text().lower() for h in headings)
        keyword_in_first_para = keyword in paragraphs[0].get_text().lower() if paragraphs else False

        return {
            "in_title": keyword_in_title,
            "in_headings": keyword_in_headings,
            "in_first_paragraph": keyword_in_first_para
        }

    except Exception as e:
        return {
            "in_title": False,
            "in_headings": False,
            "in_first_paragraph": False,
            "error": str(e)
        }
