from flask import Flask, request, jsonify, send_from_directory
import requests
import os

from backend.analyzer.http import fetch_url
from backend.analyzer.html import analyze_html
from backend.analyzer.checks import run_checks


app = Flask(__name__, static_folder=None)


FRONTEND_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "frontend")
)


@app.get("/")
def home():
    return send_from_directory(FRONTEND_DIR, "index.html")


@app.get("/static/<path:filename>")
def static_files(filename):
    return send_from_directory(FRONTEND_DIR, filename)


@app.post("/analyze")
def analyze():
    data = request.get_json()

    if not data or "url" not in data:
        return jsonify({
            "error": "URL is required"
        }), 400

    url = data["url"]

    try:
        result = fetch_url(url)

        html_analysis = analyze_html(result["html"])
        issues = run_checks(result["html"])

        return jsonify({
            "url": result["final_url"],
            "status_code": result["status_code"],
            "content_type": result["content_type"],
            "html": html_analysis,
            "issues": issues,
        })

    except requests.RequestException:
        return jsonify({
            "error": "Could not access URL"
        }), 502


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
