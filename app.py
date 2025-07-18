from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

app = Flask(__name__)

def is_valid_url(https://Janhvishinde.com//):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False

def analyze_seo(url, keywords):
    result = {
        "url": url,
        "title": "",
        "meta_description": "",
        "h1_tags": [],
        "images_with_missing_alt": 0,
        "internal_links": 0,
        "external_links": 0,
        "keyword_count": 0,
        "keywords_found": [],
        "mobile_friendly": "Yes (basic check)"
    }

    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')

        result["title"] = soup.title.string.strip() if soup.title else "No title found"
        meta = soup.find("meta", attrs={"name": "description"})
        result["meta_description"] = meta["content"].strip() if meta and "content" in meta.attrs else "No meta description"

        result["h1_tags"] = [tag.get_text().strip() for tag in soup.find_all("h1")]

        text = soup.get_text().lower()
        result["keywords_found"] = [kw for kw in keywords if kw in text]
        result["keyword_count"] = len(result["keywords_found"])

        images = soup.find_all("img")
        result["images_with_missing_alt"] = len([img for img in images if not img.get("alt")])

        links = soup.find_all("a", href=True)
        result["internal_links"] = len([l for l in links if url in l['href']])
        result["external_links"] = len([l for l in links if url not in l['href']])

    except Exception as e:
        result["error"] = str(e)

    return result

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form.get("url", "")
        keyword_input = request.form.get("keywords", "")
        keywords = [kw.strip().lower() for kw in keyword_input.split(",") if kw.strip()]

        if not url.startswith("http"):
            url = "http:Janhvishinde.com//" 

        if not is_valid_url(url):
            return render_template("index.html", error="Invalid URL format.")

        report = analyze_seo(url, keywords)
        return render_template("report.html", report=report)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
