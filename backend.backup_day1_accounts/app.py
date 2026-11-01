from flask import Flask, request, jsonify, send_from_directory
import requests
import os

from backend.analyzer.http import fetch_url
from backend.analyzer.html import analyze_html
from backend.analyzer.checks import run_checks
from backend.ai.service import AIService

app = Flask(__name__, static_folder=None)
ai_service = AIService()

FRONTEND_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "frontend")
)


@app.get("/")
def home():
    return send_from_directory(FRONTEND_DIR, "index.html")


STATIC_DIR = os.path.join(FRONTEND_DIR, "static")

@app.get("/static/themes/<path:filename>")
def static_theme_files(filename):
    return send_from_directory(
        os.path.join(STATIC_DIR, "themes"),
        filename
    )

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
        issues = run_checks(
            result["html"],
            result["final_url"]
        )

        # A Claude apenas comenta os checks encontrados.
        # Se a IA estiver indisponível, a análise continua normalmente.
        try:
            ai_comments = ai_service.comment_checks(issues)

            comments_by_check = {
                item.get("check"): item.get("comment")
                for item in ai_comments
            }

            for issue in issues:
                check_id = issue.get("check")

                if check_id in comments_by_check:
                    issue["ai_comment"] = comments_by_check[check_id]

        except Exception as e:
            print(f"CLAUDE ERROR: {e}")

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


@app.post("/api/chat")
def chat():
    data = request.get_json()

    if not data or "message" not in data:
        return jsonify({
            "error": "Message is required"
        }), 400

    message = data["message"]
    context = data.get("context")

    try:
        response = ai_service.ask_chat(
            message=message,
            context=context
        )

        return jsonify({
            "response": response
        })

    except Exception as e:
        print(f"OPENAI ERROR: {e}")

        return jsonify({
            "error": "AI service unavailable"
        }), 503


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
