from flask import Flask, jsonify, request, Response, render_template
import requests
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search')
def search():
    query = request.args.get('query')
    if query:
        try:
            response = requests.get(f'https://api.github.com/search/repositories?q={query}')
            response.raise_for_status() 
            return jsonify(response.json())
        except requests.exceptions.RequestException as e:
            app.logger.error(f"Error fetching data from GitHub API: {str(e)}")
            return jsonify({"error": "Failed to fetch data from GitHub API"}), 500
    else:
        return jsonify([])

@app.route('/download')
def download():
    url = request.args.get('url')
    if url:
        download_url = url.replace('api.github.com/repos', 'github.com').replace('/{archive_format}{/ref}', '/archive/master.zip')
        try:
            response = requests.get(download_url, allow_redirects=True)
            if response.status_code == 200:
                return Response(
                    response.content,
                    headers={
                        'Content-Disposition': 'attachment; filename=generatedcode.zip',
                        'Content-Type': 'application/zip'
                    }
                )
            else:
                return f"Error downloading zip file: {response.status_code}"
        except Exception as e:
            return f"Error downloading zip file: {str(e)}"
    else:
        return "Invalid URL"

@app.route('/repo_details.html')
def repo_details():
    return render_template('repo_details.html')

@app.route('/home.html')
def home():
    return render_template('home.html')

@app.route('/repo_data')
def repo_data():
    query = request.args.get('query')
    if query:
        try:
            response = requests.get(f'https://api.github.com/search/repositories?q={query}')
            response.raise_for_status() 
            data = response.json()['items']
            return jsonify(data)
        except requests.exceptions.RequestException as e:
            app.logger.error(f"Error fetching data from GitHub API: {str(e)}")
            return jsonify({"error": "Failed to fetch data from GitHub API"}), 500
    else:
        return jsonify([]) 

    
if __name__ == '__main__':
    app.run(debug=True)