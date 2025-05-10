import requests
from bs4 import BeautifulSoup
import json
import matplotlib.pyplot as plt
import xlsxwriter
import os
import time
import re
from collections import Counter

# SEO check modules
from seo_checks import mobile_check, speed_check, robots_txt, sitemap_check, social_links, mobile_audit

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

# Streamlit-safe logger
def log(msg, st=None):
    print(msg)
    if st:
        st.info(msg)

def fetch_page(url, st=None):
    for attempt in range(3):
        try:
            log(f"🌐 Fetching: {url}", st)
            response = requests.get(url, headers=HEADERS)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            log(f"⚠️ Error fetching page: {e}", st)
            time.sleep(2)
    return None

def parse_page(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    titles = [tag.get_text(strip=True) for tag in soup.select("h2 a span")]
    price_blocks = soup.select(".a-price")

    top_items = []
    for i in range(min(15, len(titles), len(price_blocks))):
        try:
            whole = price_blocks[i].select_one('.a-price-whole')
            fraction = price_blocks[i].select_one('.a-price-fraction')
            price_text = whole.get_text(strip=True).replace(',', '') if whole else "0"
            fraction_text = fraction.get_text(strip=True) if fraction else "00"
            if price_text.isdigit():
                price = int(price_text) + float("0." + fraction_text)
                top_items.append((titles[i], price))
        except Exception:
            continue
    return titles, top_items[:10]

def extract_top_keywords(titles, top_n=6):
    all_words = []
    for title in titles:
        words = re.findall(r'\b\w+\b', title.lower())
        all_words.extend(words)
    stopwords = {"for", "with", "and", "the", "from", "inch", "cm", "in", "to", "a", "on", "by", "of", "at", "it", "is"}
    filtered = [word for word in all_words if word not in stopwords and len(word) > 2]
    return dict(Counter(filtered).most_common(top_n))

def categorize_by_brand(titles):
    brands = {"Samsung": [], "iPhone": [], "Motorola": [], "Realme": [], "Poco": [], "Moto": []}
    for title in titles:
        lower = title.lower()
        for brand in brands:
            if brand.lower() in lower:
                brands[brand].append(title)
    return brands

def save_results(results, keywords, products, brands):
    os.makedirs("output", exist_ok=True)
    wb = xlsxwriter.Workbook("output/report.xlsx")
    ws = wb.add_worksheet("SEO Report")

    ws.write(0, 0, "SEO Check")
    ws.write(0, 1, "Result")
    for i, (k, v) in enumerate(results.items(), 1):
        ws.write(i, 0, k)
        ws.write(i, 1, str(v))

    row = len(results) + 2
    ws.write(row, 0, "Keyword")
    ws.write(row, 1, "Count")
    for kw, count in keywords.items():
        row += 1
        ws.write(row, 0, kw)
        ws.write(row, 1, count)

    row += 2
    ws.write(row, 0, "Product")
    ws.write(row, 1, "Price")
    for title, price in products:
        row += 1
        ws.write(row, 0, title)
        ws.write(row, 1, price)

    brand_ws = wb.add_worksheet("Brand Data")
    brand_ws.write(0, 0, "Brand")
    brand_ws.write(0, 1, "Matching Titles")
    r = 1
    for brand, models in brands.items():
        if models:
            brand_ws.write(r, 0, brand)
            brand_ws.write(r, 1, "\n".join(models))
            r += 1

    wb.close()

    with open("output/seo_report.json", "w") as f:
        json.dump({
            "SEO Checks": results,
            "Keywords": keywords,
            "Products": products,
            "Brands": brands
        }, f, indent=4)

def plot_keywords(keywords):
    plt.figure(figsize=(8, 6))

    if not keywords:
        plt.text(0.5, 0.5, 'No keyword data found', fontsize=14, ha='center')
        plt.xticks([])
        plt.yticks([])
    else:
        plt.bar(keywords.keys(), keywords.values(), color='skyblue')
        plt.title("Top Keywords in Titles")
        plt.xlabel("Keyword")
        plt.ylabel("Count")

    plt.tight_layout()
    plt.savefig("output/keyword_frequency.png")
    plt.close()

def plot_prices(products):
    if not products: return
    titles = [title[:30] + '...' if len(title) > 30 else title for title, _ in products]
    prices = [price for _, price in products]
    plt.figure(figsize=(10, 6))
    plt.barh(titles, prices, color='orange')
    plt.xlabel("Price")
    plt.title("Top Product Prices")
    plt.tight_layout()
    plt.savefig("output/product_price_barchart.png")
    plt.close()

def plot_brands(brands):
    counts = {brand: len(models) for brand, models in brands.items() if models}
    if not counts: return
    plt.figure(figsize=(8, 6))
    plt.pie(counts.values(), labels=counts.keys(), autopct="%1.1f%%", startangle=140)
    plt.title("Brand Share in Results")
    plt.tight_layout()
    plt.savefig("output/smartphone_brand_distribution.png")
    plt.close()

# 🚀 Main analysis function
def seo_analysis(url, st=None):
    log(f"🚀 Starting SEO analysis for: {url}", st)

    html = fetch_page(url, st)
    if not html:
        log("❌ Failed to fetch page content.", st)
        return

    titles, products = parse_page(html)
    log(f"📦 Titles scraped: {len(titles)}", st)

    log("🔍 Checking Mobile Friendliness...", st)
    mobile = mobile_check.is_mobile_friendly(url)

    log("🚀 Checking Page Speed...", st)
    speed = speed_check.check_speed(url)

    log("📂 Checking Robots.txt...", st)
    robots = robots_txt.check_robots_txt(url)

    log("📄 Checking Sitemap.xml...", st)
    sitemap = sitemap_check.check_sitemap(url)

    log("🔗 Checking Social Media Links...", st)
    social = social_links.check_social_links(html)

    log("📱 Performing Mobile SEO Audit...", st)
    audit = mobile_audit.perform_mobile_audit(url)

    keywords = extract_top_keywords(titles)
    brands = categorize_by_brand(titles)

    results = {
        "Mobile Friendliness": mobile,
        "Page Speed": speed,
        "Robots.txt": robots,
        "Sitemap.xml": sitemap,
        "Social Links": social,
        "Mobile SEO Audit": audit
    }

    save_results(results, keywords, products, brands)
    plot_keywords(keywords)
    plot_prices(products)
    plot_brands(brands)

    log("✅ SEO Analysis completed and all files saved.", st)

# 📁 Output paths to use in Streamlit
output_data_path = {
    "excel": "output/report.xlsx",
    "json": "output/seo_report.json",
    "keyword_chart": "output/keyword_frequency.png",
    "price_chart": "output/product_price_barchart.png",
    "brand_chart": "output/smartphone_brand_distribution.png"
}

# 🧪 Run directly for testing
if __name__ == "__main__":
    seo_analysis("https://www.amazon.in/s?k=smartphones")
