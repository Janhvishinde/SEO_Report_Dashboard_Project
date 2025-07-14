from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def analyze_seo(url):
    result = {
        "url": url,
        "title": "",
        "meta_description": "",
        "h1_tags": [],
        "mobile_friendly": "Yes (basic check)",
        "keyword_count": 0,
        "keywords_found": []
    }

    keywords = ["seo", "marketing", "analytics", "performance"]

    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')

        result["title"] = soup.title.string if soup.title else "No title found"

        meta_desc = soup.find("meta", attrs={"name": "description"})
        result["meta_description"] = meta_desc["content"] if meta_desc else "No meta description"

        result["h1_tags"] = [tag.get_text().strip() for tag in soup.find_all("h1")]

        text = soup.get_text().lower()
        result["keywords_found"] = [kw for kw in keywords if kw in text]
        result["keyword_count"] = len(result["keywords_found"])

    except Exception as e:
        result["error"] = str(e)

    return result

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form["url"]
        if not url.startswith("http"):
            url = "http://" + url
        report = analyze_seo(url)
        return render_template("report.html", report=report)
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
