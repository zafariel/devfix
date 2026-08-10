from bs4 import BeautifulSoup


def run_checks(html):
    soup = BeautifulSoup(html, "html.parser")

    issues = []

    # 1. Title
    title = soup.find("title")

    if not title or not title.get_text(strip=True):
        issues.append({
            "id": "missing-title",
            "severity": "high",
            "category": "seo",
            "message": "A página não possui uma tag <title>.",
            "recommendation": "Adicione um <title> descritivo dentro do <head>."
        })

    # 2. Meta description
    description = soup.find(
        "meta",
        attrs={"name": "description"}
    )

    if not description or not description.get("content", "").strip():
        issues.append({
            "id": "missing-description",
            "severity": "medium",
            "category": "seo",
            "message": "A página não possui uma meta description.",
            "recommendation": "Adicione uma meta description relevante para a página."
        })

    # 3. Imagens sem alt
    images_without_alt = []

    for image in soup.find_all("img"):
        if not image.get("alt"):
            images_without_alt.append(
                image.get("src", "")
            )

    if images_without_alt:
        issues.append({
            "id": "images-missing-alt",
            "severity": "medium",
            "category": "accessibility",
            "message": f"{len(images_without_alt)} imagem(ns) não possui(em) atributo alt.",
            "recommendation": "Adicione um atributo alt descritivo às imagens."
        })

    return issues
