from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
from flask_cors import CORS
from duckduckgo_search import DDGS

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "Web Scraper is live!"

@app.route('/scrape', methods=['GET'])
def scrape():
    url = request.args.get('url')
    keyword = request.args.get('keyword')

    result = []

    try:
        if url:
            response = requests.get(url, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            for i, tag in enumerate(soup.find_all(['p', 'h1', 'h2', 'li'], limit=30)):
                result.append({'index': i + 1, 'content': tag.text.strip()})
            return jsonify({'status': 'success', 'data': result})

        elif keyword:
            with DDGS() as ddgs:
                for i, r in enumerate(ddgs.text(keyword, max_results=5)):
                    result.append({'index': i + 1, 'title': r['title'], 'link': r['href']})
            return jsonify({'status': 'success', 'data': result})

        else:
            return jsonify({'status': 'error', 'message': 'No URL or keyword provided'})

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
