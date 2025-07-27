from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # allows access from your WordPress

@app.route('/')
def home():
    return "Web Scraper is live!"

@app.route('/scrape', methods=['GET'])
def scrape():
    url = request.args.get('url')
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')

        result = []
        for i, tag in enumerate(soup.find_all(['p', 'h1', 'h2', 'li'], limit=30)):
            result.append({'index': i + 1, 'content': tag.text.strip()})

        return jsonify({'status': 'success', 'data': result})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})
