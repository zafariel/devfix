from bs4 import BeautifulSoup


def analyze_html(html):
    soup = BeautifulSoup(html, "html.parser")

    title = soup.title.string.strip() if soup.title and soup.title.string else None

    description_tag = soup.find(
        "meta",
        attrs={"name": "description"}
    )

    description = (
        description_tag.get("content", "").strip()
        if description_tag
        else None
    )

    images = soup.find_all("img")
    links = soup.find_all("a")

    return {
        "title": title,
        "description": description,
        "images": len(images),
        "links": len(links),
    }
