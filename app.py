import os
from flask import Flask, render_template, request
import requests
from datetime import datetime

app = Flask(__name__)

def get_http_status(url):
    try:
        response = requests.head(url)
        return response.status_code
    except requests.RequestException as e:
        return None

def get_naver_search_results(query, client_id, client_secret, start=1, display=20):
    base_url = "https://openapi.naver.com/v1/search/webkr.json"
    headers = {
        "X-Naver-Client-Id": client_id,
        "X-Naver-Client-Secret": client_secret
    }
    params = {
        "query": query,
        "display": display,  # 가져올 결과 개수
        "start": start,  # 시작 위치 (1부터 시작)
    }
    try:
        response = requests.get(base_url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print("Error:", e)
        return None

@app.route('/', methods=['GET'])
def index():
    query = request.args.get('query')
    if query:
        client_id = "a5uQFjClEURaL3o6JbbT"  # 네이버 API의 클라이언트 ID
        client_secret = "1Inp0lfzmQ"  # 네이버 API의 클라이언트 시크릿
        start_page = 1
        num_results = 20  # 가져올 결과 개수

        search_results = get_naver_search_results(query, client_id, client_secret, start=start_page, display=num_results)
        if not search_results or not search_results.get("items"):
            error_message = "검색 결과를 가져올 수 없습니다."
            return render_template('index.html', error_message=error_message)
        else:
            results = []
            for result in search_results["items"]:
                link = result['link']
                http_status = get_http_status(link)
                results.append({
                    'title': result['title'],
                    'link': link,
                    'http_status': http_status
                })
            return render_template('index.html', query=query, results=results)
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
