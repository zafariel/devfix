import requests


def fetch_url(url):
    response = requests.get(
        url,
        timeout=10,
        headers={
            "User-Agent": "DEVFIX/0.1"
        }
    )

    return {
        "status_code": response.status_code,
        "final_url": response.url,
        "content_type": response.headers.get("Content-Type"),
        "html": response.text,
    }
