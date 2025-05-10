import requests
from urllib.parse import urlparse

def check_sitemap(url):
    try:
        parsed = urlparse(url)
        base_url = f"{parsed.scheme}://{parsed.netloc}"
        sitemap_url = f"{base_url}/sitemap.xml"

        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(sitemap_url, headers=headers)

        if response.status_code == 200 and ("<urlset" in response.text or "<sitemapindex" in response.text):
            return {
                "sitemap_found": True,
                "sitemap_url": sitemap_url
            }
        else:
            return {
                "sitemap_found": False,
                "sitemap_url": sitemap_url
            }

    except Exception as e:
        return {
            "sitemap_found": False,
            "sitemap_url": None,
            "error": str(e)
        }
