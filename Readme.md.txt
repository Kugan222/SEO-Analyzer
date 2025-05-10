SEO and Brand Analyzer for Amazon Listings

Project Summary

This Python-based tool is designed to analyze Amazon product listings through a provided search URL. It scrapes product data such as titles and prices, performs essential SEO audits, and provides visual analytics in the form of charts and downloadable reports. The tool is equipped with both a command-line script and a web interface powered by Streamlit.


Demo

A working demonstration of the tool includes:
- Extraction of top product titles and pricing
- Keyword frequency chart
- Brand distribution visualization
- SEO reports in Excel and JSON formats
Watch Demo Video:(https://drive.google.com/file/d/1o68AYOmKU2C77OU4UwTcaf2_nVUcmxzu/view?usp=sharing)

How to Run Locally

1. Clone the repository
   git clone https://github.com/Kugan222/seo-analyzer.git
   cd seo-analyzer

2. Install required packages
   pip install -r requirements.txt

3. Run the analysis script
   python core_scraper.py

4. Launch the Streamlit dashboard
   streamlit run app.py

5. View results
   Reports are saved to the output/ folder
   Includes: Excel report, JSON data, and image graphs

Technologies Used

Python 3.x – Core programming language
Requests & BeautifulSoup – Web scraping and HTML parsing
Matplotlib – Visual representation of product trends
XlsxWriter – Automated Excel report generation
Streamlit – Interactive frontend dashboard
Regex & JSON – Data formatting and keyword extraction

Future Scope

Extend support beyond Amazon: the architecture is adaptable to work with any e-commerce or content-based website.
Enhance keyword detection using natural language processing for deeper insights.
Introduce Google SERP integration for competitive keyword ranking.
Add multi-language support and dynamic keyword relevance scoring.
Deploy on Streamlit Cloud or platforms like Render for real-time public access.

This tool serves as a foundation for more comprehensive SEO auditing systems in both academic and commercial use cases.

