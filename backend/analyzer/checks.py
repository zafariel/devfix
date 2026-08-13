from bs4 import BeautifulSoup


def run_checks(html, url):
    soup = BeautifulSoup(html, "html.parser")

    issues = []

    # 1. Title ausente
    title = soup.find("title")
    
    if not title or not title.get_text(strip=True):
        issues.append({
            "id": "missing-title",
            "severity": "high",
            "category": "seo",
            "message": "A página não possui uma tag <title>.",
            "problem": "A página não possui um título definido.",
            "recommendation": "Adicione um <title> descritivo dentro do <head>.",
            "example": "<title>Título da página</title>"
        })
    
    
    # 2. Meta description ausente
    description = soup.find(
        "meta",
        attrs={"name": "description"}
    )
    
    if not description or not description.get("content", "").strip():
        issues.append({
            "id": "missing-description",
            "severity": "medium",
            "category": "seo",
            "message": "Meta description ausente",
            "problem": "Sua página não fornece uma descrição para mecanismos de busca.",
            "recommendation": "Adicione uma descrição relevante dentro do <head>.",
            "example": '<meta name="description" content="Descrição da página">'
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
            "problem": "Uma ou mais imagens não possuem um atributo alt.",
            "recommendation": "Adicione um atributo alt descritivo a cada imagem.",
            "example": '<img src="imagem.jpg" alt="Descrição da imagem">'
        })
    
    
    # 4. H1 ausente
    h1s = soup.find_all("h1")
    
    if len(h1s) == 0:
        issues.append({
            "id": "missing-h1",
            "severity": "high",
            "category": "html",
            "message": "H1 ausente",
            "problem": "A página não possui um título principal H1.",
            "recommendation": "Adicione um elemento <h1> que descreva claramente o conteúdo principal.",
            "example": "<h1>Título principal da página</h1>"
        })
    
    
    # 5. Múltiplos H1
    if len(h1s) > 1:
        issues.append({
            "id": "multiple-h1",
            "severity": "medium",
            "category": "html",
            "message": f"A página possui {len(h1s)} elementos <h1>.",
            "problem": "A página possui mais de um título principal H1.",
            "recommendation": "Revise a hierarquia dos títulos e mantenha um H1 principal.",
            "example": "<h1>Título principal</h1>"
        })
    
    
    # 6. HTML sem lang
    html_tag = soup.find("html")
    
    if not html_tag or not html_tag.get("lang"):
        issues.append({
            "id": "missing-lang",
            "severity": "medium",
            "category": "accessibility",
            "message": "O idioma da página não foi definido.",
            "problem": "O elemento <html> não possui um atributo lang.",
            "recommendation": "Defina o idioma principal da página usando o atributo lang.",
            "example": '<html lang="pt-BR">'
        })
    
    
    # 7. Lang inválido ou incompleto
    if html_tag and html_tag.get("lang"):
        lang = html_tag.get("lang").strip()
    
        if len(lang) < 2:
            issues.append({
                "id": "invalid-lang",
                "severity": "low",
                "category": "accessibility",
                "message": "O atributo lang parece inválido.",
                "problem": "O idioma definido possui um valor muito curto.",
                "recommendation": "Use um código de idioma válido, como pt-BR ou en-US.",
                "example": '<html lang="pt-BR">'
            })
    
    
    # 8. Charset ausente
    charset = soup.find("meta", charset=True)
    
    if not charset:
        issues.append({
            "id": "missing-charset",
            "severity": "medium",
            "category": "html",
            "message": "Charset ausente.",
            "problem": "A página não define explicitamente o conjunto de caracteres.",
            "recommendation": "Adicione uma declaração de charset no <head>.",
            "example": '<meta charset="UTF-8">'
        })
    
    
    # 9. Charset diferente de UTF-8
    if charset:
        charset_value = charset.get("charset", "").strip().upper()
    
        if charset_value != "UTF-8":
            issues.append({
                "id": "non-utf8-charset",
                "severity": "low",
                "category": "html",
                "message": "A página não utiliza UTF-8.",
                "problem": f"O charset encontrado é {charset_value}.",
                "recommendation": "Prefira UTF-8 para garantir melhor compatibilidade de caracteres.",
                "example": '<meta charset="UTF-8">'
            })
    
    
    # 10. Viewport ausente
    viewport = soup.find(
        "meta",
        attrs={"name": "viewport"}
    )
    
    if not viewport or not viewport.get("content", "").strip():
        issues.append({
            "id": "missing-viewport",
            "severity": "medium",
            "category": "mobile",
            "message": "Meta viewport ausente.",
            "problem": "A página não define corretamente a viewport para dispositivos móveis.",
            "recommendation": "Adicione uma meta viewport no <head>.",
            "example": '<meta name="viewport" content="width=device-width, initial-scale=1.0">'
        })
    
    # 11. <main> ausente
    main_tag = soup.find("main")
    
    if not main_tag:
        issues.append({
            "id": "missing-main",
            "severity": "medium",
            "category": "html",
            "message": "A página não possui um elemento <main>.",
            "problem": "O conteúdo principal da página não está identificado semanticamente.",
            "recommendation": "Adicione um elemento <main> envolvendo o conteúdo principal.",
            "example": "<main>Conteúdo principal</main>"
        })
    
    
    # 12. <header> ausente
    header_tag = soup.find("header")
    
    if not header_tag:
        issues.append({
            "id": "missing-header",
            "severity": "low",
            "category": "html",
            "message": "A página não possui um elemento <header>.",
            "problem": "A página não possui uma região semântica de cabeçalho.",
            "recommendation": "Considere utilizar um elemento <header> para identificar o cabeçalho.",
            "example": "<header><h1>Meu site</h1></header>"
        })
    
    
    # 13. <footer> ausente
    footer_tag = soup.find("footer")
    
    if not footer_tag:
        issues.append({
            "id": "missing-footer",
            "severity": "low",
            "category": "html",
            "message": "A página não possui um elemento <footer>.",
            "problem": "A página não possui uma região semântica de rodapé.",
            "recommendation": "Considere utilizar um elemento <footer> para informações de rodapé.",
            "example": "<footer>© 2026 Meu site</footer>"
        })
    
    
    # 14. <nav> sem links
    nav_tags = soup.find_all("nav")
    
    for nav in nav_tags:
        links = nav.find_all("a")
    
        if not links:
            issues.append({
                "id": "nav-without-links",
                "severity": "medium",
                "category": "accessibility",
                "message": "Um elemento <nav> não possui links.",
                "problem": "A região de navegação não contém links para navegação.",
                "recommendation": "Adicione links de navegação dentro do elemento <nav> ou remova o <nav> se ele não for necessário.",
                "example": '<nav><a href="/">Início</a></nav>'
            })
            break
    
    
    # 15. <a> sem href
    links_without_href = []
    
    for link in soup.find_all("a"):
        if not link.get("href"):
            links_without_href.append(link)
    
    if links_without_href:
        issues.append({
            "id": "links-missing-href",
            "severity": "medium",
            "category": "html",
            "message": f"{len(links_without_href)} link(s) não possui(em) href.",
            "problem": "Um ou mais elementos <a> não possuem um destino definido.",
            "recommendation": "Adicione um atributo href válido aos links.",
            "example": '<a href="/contato">Contato</a>'
        })
    
    
    # 16. <a> sem texto acessível
    links_without_text = []
    
    for link in soup.find_all("a"):
        text = link.get_text(" ", strip=True)
    
        if not text and not link.find("img", alt=True):
            links_without_text.append(link)
    
    if links_without_text:
        issues.append({
            "id": "links-without-accessible-text",
            "severity": "medium",
            "category": "accessibility",
            "message": f"{len(links_without_text)} link(s) não possui(em) texto acessível.",
            "problem": "Um ou mais links não possuem texto que identifique sua finalidade.",
            "recommendation": "Adicione texto descritivo ou uma alternativa acessível ao link.",
            "example": '<a href="/contato">Entre em contato</a>'
        })
    
    
    # 17. <img> sem src
    images_without_src = []
    
    for image in soup.find_all("img"):
        if not image.get("src"):
            images_without_src.append(image)
    
    if images_without_src:
        issues.append({
            "id": "images-missing-src",
            "severity": "medium",
            "category": "html",
            "message": f"{len(images_without_src)} imagem(ns) não possui(em) src.",
            "problem": "Uma ou mais imagens não possuem um caminho para o arquivo.",
            "recommendation": "Adicione um atributo src válido para cada imagem.",
            "example": '<img src="imagem.jpg" alt="Descrição da imagem">'
        })
    
    
    # 18. <img> com alt vazio
    images_with_empty_alt = []
    
    for image in soup.find_all("img"):
        if image.has_attr("alt") and image.get("alt", "").strip() == "":
            images_with_empty_alt.append(image)
    
    if images_with_empty_alt:
        issues.append({
            "id": "images-empty-alt",
            "severity": "low",
            "category": "accessibility",
            "message": f"{len(images_with_empty_alt)} imagem(ns) possui(em) alt vazio.",
            "problem": "Uma ou mais imagens possuem alt vazio.",
            "recommendation": "Use um texto alternativo descritivo quando a imagem tiver significado. Para imagens puramente decorativas, alt vazio pode ser apropriado.",
            "example": '<img src="produto.jpg" alt="Tênis esportivo preto">'
        })
    
    
    # 19. <script> externo sem src válido
    scripts_without_src = []
    
    for script in soup.find_all("script"):
        if not script.get_text(strip=True) and not script.get("src"):
            scripts_without_src.append(script)
    
    if scripts_without_src:
        issues.append({
            "id": "external-script-missing-src",
            "severity": "low",
            "category": "javascript",
            "message": f"{len(scripts_without_src)} script(s) externo(s) não possui(em) src.",
            "problem": "Um elemento <script> parece estar sendo usado como script externo, mas não possui um caminho src.",
            "recommendation": "Adicione um atributo src válido ou coloque o JavaScript diretamente dentro do elemento <script>.",
            "example": '<script src="/static/app.js"></script>'
        })
    
    
    # 20. CSS externo sem href
    stylesheet_links_without_href = []
    
    for link in soup.find_all("link"):
        rel = link.get("rel", [])
    
        if "stylesheet" in rel and not link.get("href"):
            stylesheet_links_without_href.append(link)
    
    if stylesheet_links_without_href:
        issues.append({
            "id": "stylesheet-missing-href",
            "severity": "medium",
            "category": "css",
            "message": f"{len(stylesheet_links_without_href)} folha(s) de estilo não possui(em) href.",
            "problem": "Uma folha de estilo foi declarada sem indicar o arquivo CSS.",
            "recommendation": "Adicione um atributo href apontando para o arquivo CSS.",
            "example": '<link rel="stylesheet" href="/static/style.css">'
        })
    
    # 23. Hierarquia de headings problemática
    headings = soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"])
    
    previous_level = None
    
    for heading in headings:
        current_level = int(heading.name[1])
    
        if previous_level is not None and current_level > previous_level + 1:
            issues.append({
                "id": "heading-hierarchy",
                "severity": "medium",
                "category": "html",
                "message": "Hierarquia de headings problemática.",
                "problem": f"O documento passou de H{previous_level} para H{current_level}.",
                "recommendation": "Evite saltos desnecessários na hierarquia dos títulos.",
                "example": "<h2>Seção</h2><h3>Subseção</h3>"
            })
            break
    
        previous_level = current_level
    
    
    # 24. Saltos grandes na hierarquia
    previous_level = None
    
    for heading in headings:
        current_level = int(heading.name[1])
    
        if previous_level is not None and current_level - previous_level > 1:
            issues.append({
                "id": "heading-level-skip",
                "severity": "low",
                "category": "accessibility",
                "message": "Salto de nível nos headings.",
                "problem": f"Foi encontrado um salto de H{previous_level} para H{current_level}.",
                "recommendation": "Organize os headings em uma sequência hierárquica lógica.",
                "example": "<h2>Seção</h2><h3>Subseção</h3>"
            })
            break
    
        previous_level = current_level
    
    
    # 25. Página sem headings
    if not headings:
        issues.append({
            "id": "missing-headings",
            "severity": "medium",
            "category": "html",
            "message": "A página não possui headings.",
            "problem": "Nenhum título estrutural foi encontrado na página.",
            "recommendation": "Adicione headings para organizar o conteúdo.",
            "example": "<h1>Título principal</h1>"
        })
    
    
    # 26. Button sem texto acessível
    buttons_without_text = []
    
    for button in soup.find_all("button"):
        text = button.get_text(" ", strip=True)
    
        if not text and not button.get("aria-label"):
            buttons_without_text.append(button)
    
    if buttons_without_text:
        issues.append({
            "id": "button-without-text",
            "severity": "medium",
            "category": "accessibility",
            "message": f"{len(buttons_without_text)} botão(ões) sem texto acessível.",
            "problem": "Um ou mais botões não possuem texto ou aria-label identificando sua função.",
            "recommendation": "Adicione texto descritivo ou aria-label.",
            "example": '<button aria-label="Abrir menu">☰</button>'
        })
    
    
    # 27. Input sem label
    inputs_without_label = []
    
    for input_element in soup.find_all("input"):
        input_id = input_element.get("id")
    
        if not input_id:
            inputs_without_label.append(input_element)
            continue
    
        label = soup.find("label", attrs={"for": input_id})
    
        if not label:
            inputs_without_label.append(input_element)
    
    if inputs_without_label:
        issues.append({
            "id": "input-without-label",
            "severity": "medium",
            "category": "accessibility",
            "message": f"{len(inputs_without_label)} campo(s) de entrada sem label.",
            "problem": "Um ou mais campos não possuem uma label associada.",
            "recommendation": "Associe cada input a uma label.",
            "example": '<label for="email">E-mail</label><input id="email" type="email">'
        })
    
    
    # 28. Form sem method
    for form in soup.find_all("form"):
        if not form.get("method"):
            issues.append({
                "id": "form-missing-method",
                "severity": "low",
                "category": "html",
                "message": "Formulário sem método definido.",
                "problem": "O formulário não possui o atributo method.",
                "recommendation": "Defina explicitamente o método do formulário.",
                "example": '<form method="post">'
            })
    
    
    # 29. Form sem action
    for form in soup.find_all("form"):
        if not form.get("action"):
            issues.append({
                "id": "form-missing-action",
                "severity": "low",
                "category": "html",
                "message": "Formulário sem action definido.",
                "problem": "O formulário não possui um destino definido para o envio.",
                "recommendation": "Defina um atributo action apropriado.",
                "example": '<form action="/enviar" method="post">'
            })
    
    
    # 30. Meta robots ausente
    robots = soup.find(
        "meta",
        attrs={"name": "robots"}
    )
    
    if not robots:
        issues.append({
            "id": "missing-robots",
            "severity": "low",
            "category": "seo",
            "message": "Meta robots ausente.",
            "problem": "A página não define instruções específicas para robôs de mecanismos de busca.",
            "recommendation": "Considere adicionar uma meta robots quando houver necessidade de controlar a indexação.",
            "example": '<meta name="robots" content="index, follow">'
        })
    
    # 31. Canonical ausente
    canonical = soup.find(
        "link",
        attrs={"rel": "canonical"}
    )
    
    if not canonical or not canonical.get("href", "").strip():
        issues.append({
            "id": "missing-canonical",
            "severity": "low",
            "category": "seo",
            "message": "Canonical ausente.",
            "problem": "A página não possui uma URL canônica definida.",
            "recommendation": "Adicione uma URL canônica quando necessário.",
            "example": '<link rel="canonical" href="https://exemplo.com/pagina">'
        })
    
    
    # 32. Title muito curto
    if title and title.get_text(strip=True):
        title_text = title.get_text(" ", strip=True)
    
        if len(title_text) < 10:
            issues.append({
                "id": "short-title",
                "severity": "low",
                "category": "seo",
                "message": "O título da página é muito curto.",
                "problem": f"O title possui apenas {len(title_text)} caracteres.",
                "recommendation": "Crie um título mais descritivo e específico.",
                "example": "<title>DEVFIX — Diagnóstico para sites</title>"
            })
    
    
    # 33. Title muito longo
    if title and title.get_text(strip=True):
        title_text = title.get_text(" ", strip=True)
    
        if len(title_text) > 60:
            issues.append({
                "id": "long-title",
                "severity": "low",
                "category": "seo",
                "message": "O título da página é muito longo.",
                "problem": f"O title possui {len(title_text)} caracteres.",
                "recommendation": "Reduza o título para deixá-lo mais objetivo.",
                "example": "<title>DEVFIX — Diagnóstico para sites</title>"
            })
    
    
    # 34. Meta description muito curta
    if description and description.get("content", "").strip():
        description_text = description.get("content", "").strip()
    
        if len(description_text) < 50:
            issues.append({
                "id": "short-description",
                "severity": "low",
                "category": "seo",
                "message": "A meta description é muito curta.",
                "problem": f"A description possui apenas {len(description_text)} caracteres.",
                "recommendation": "Crie uma descrição mais informativa.",
                "example": '<meta name="description" content="Analise seu site com o DEVFIX e encontre problemas de SEO, acessibilidade e estrutura.">'
            })
    
    
    # 35. Meta description muito longa
    if description and description.get("content", "").strip():
        description_text = description.get("content", "").strip()
    
        if len(description_text) > 160:
            issues.append({
                "id": "long-description",
                "severity": "low",
                "category": "seo",
                "message": "A meta description é muito longa.",
                "problem": f"A description possui {len(description_text)} caracteres.",
                "recommendation": "Reduza a descrição e mantenha apenas as informações mais importantes.",
                "example": '<meta name="description" content="Analise seu site com o DEVFIX.">'
            })
    
    
    # 36. IDs duplicados
    ids = {}
    
    for element in soup.find_all(attrs={"id": True}):
        element_id = element.get("id", "").strip()
    
        if element_id:
            ids[element_id] = ids.get(element_id, 0) + 1
    
    duplicate_ids = [
        element_id
        for element_id, count in ids.items()
        if count > 1
    ]
    
    if duplicate_ids:
        issues.append({
            "id": "duplicate-ids",
            "severity": "medium",
            "category": "html",
            "message": f"{len(duplicate_ids)} ID(s) duplicado(s) encontrado(s).",
            "problem": "Existem elementos diferentes utilizando o mesmo atributo id.",
            "recommendation": "Garanta que cada ID seja único dentro da página.",
            "example": '<section id="sobre">Conteúdo</section>'
        })
    
    
    # 37. IDs vazios ou inválidos
    invalid_ids = []
    
    for element in soup.find_all(attrs={"id": True}):
        element_id = element.get("id", "").strip()
    
        if not element_id:
            invalid_ids.append(element)
    
    if invalid_ids:
        issues.append({
            "id": "empty-ids",
            "severity": "low",
            "category": "html",
            "message": f"{len(invalid_ids)} elemento(s) possui(em) ID vazio.",
            "problem": "Um ou mais elementos possuem um atributo id sem valor.",
            "recommendation": "Remova o ID se ele não for necessário ou atribua um identificador válido.",
            "example": '<section id="sobre">Conteúdo</section>'
        })
    
    
    # 38. Iframe sem title
    iframes_without_title = []
    
    for iframe in soup.find_all("iframe"):
        if not iframe.get("title", "").strip():
            iframes_without_title.append(iframe)
    
    if iframes_without_title:
        issues.append({
            "id": "iframe-missing-title",
            "severity": "medium",
            "category": "accessibility",
            "message": f"{len(iframes_without_title)} iframe(s) não possui(em) title.",
            "problem": "Um ou mais iframes não possuem uma descrição acessível.",
            "recommendation": "Adicione um atributo title descritivo ao iframe.",
            "example": '<iframe src="mapa.html" title="Mapa da localização"></iframe>'
        })
    
    
    # 39. Vídeo sem alternativa
    videos_without_accessibility = []
    
    for video in soup.find_all("video"):
        has_track = video.find("track")
        has_text = video.get_text(" ", strip=True)
    
        if not has_track and not has_text:
            videos_without_accessibility.append(video)
    
    if videos_without_accessibility:
        issues.append({
            "id": "video-without-alternative",
            "severity": "medium",
            "category": "accessibility",
            "message": f"{len(videos_without_accessibility)} vídeo(s) pode(m) não possuir alternativa acessível.",
            "problem": "O vídeo não possui uma faixa de texto ou alternativa detectável.",
            "recommendation": "Considere adicionar legendas usando <track> ou outra alternativa acessível.",
            "example": '<video controls><track kind="captions" src="legendas.vtt"></video>'
        })
    
    
    # 40. Áudio sem alternativa
    audios_without_alternative = []
    
    for audio in soup.find_all("audio"):
        has_text = audio.get_text(" ", strip=True)
    
        if not has_text:
            audios_without_alternative.append(audio)
    
    if audios_without_alternative:
        issues.append({
            "id": "audio-without-alternative",
            "severity": "low",
            "category": "accessibility",
            "message": f"{len(audios_without_alternative)} áudio(s) pode(m) não possuir alternativa.",
            "problem": "O elemento de áudio não possui uma alternativa textual detectável.",
            "recommendation": "Forneça uma alternativa textual ou uma transcrição quando apropriado.",
            "example": '<audio controls><source src="audio.mp3"></audio>'
        })
    
    # 41. HTML muito grande
    html_size = len(html.encode("utf-8"))
    
    if html_size > 500_000:
        issues.append({
            "id": "large-html",
            "severity": "medium",
            "category": "performance",
            "message": "O HTML da página é muito grande.",
            "problem": f"O documento possui aproximadamente {html_size // 1024} KB.",
            "recommendation": "Reduza o tamanho do HTML removendo conteúdo desnecessário e otimizando a estrutura.",
            "example": "Mantenha o HTML o mais enxuto possível."
        })
    
    
    # 42. Número excessivo de elementos DOM
    elements = soup.find_all()
    
    if len(elements) > 1500:
        issues.append({
            "id": "excessive-dom-elements",
            "severity": "medium",
            "category": "performance",
            "message": "A página possui muitos elementos HTML.",
            "problem": f"Foram encontrados aproximadamente {len(elements)} elementos.",
            "recommendation": "Reduza elementos desnecessários e simplifique a estrutura do DOM.",
            "example": "<main><section>Conteúdo</section></main>"
        })
    
    
    # 43. Muitos scripts externos
    external_scripts = []
    
    for script in soup.find_all("script"):
        if script.get("src"):
            external_scripts.append(script)
    
    if len(external_scripts) > 10:
        issues.append({
            "id": "too-many-external-scripts",
            "severity": "medium",
            "category": "javascript",
            "message": "A página possui muitos scripts externos.",
            "problem": f"Foram encontrados {len(external_scripts)} scripts externos.",
            "recommendation": "Revise os scripts utilizados e remova dependências desnecessárias.",
            "example": '<script src="/static/app.js"></script>'
        })
    
    
    # 44. Muitos arquivos CSS externos
    external_stylesheets = []
    
    for link in soup.find_all("link"):
        rel = link.get("rel", [])
    
        if "stylesheet" in rel and link.get("href"):
            external_stylesheets.append(link)
    
    if len(external_stylesheets) > 5:
        issues.append({
            "id": "too-many-stylesheets",
            "severity": "low",
            "category": "css",
            "message": "A página possui muitos arquivos CSS externos.",
            "problem": f"Foram encontrados {len(external_stylesheets)} arquivos CSS externos.",
            "recommendation": "Considere reduzir ou agrupar arquivos CSS quando isso fizer sentido.",
            "example": '<link rel="stylesheet" href="/static/style.css">'
        })
    
    
    # 45. Recursos HTTP em página HTTPS
    if url.startswith("https://"):
        insecure_resources = []
    
        for tag in soup.find_all(src=True):
            src = tag.get("src", "").strip()
    
            if src.startswith("http://"):
                insecure_resources.append(src)
    
        for tag in soup.find_all(href=True):
            href = tag.get("href", "").strip()
    
            if href.startswith("http://"):
                insecure_resources.append(href)
    
        if insecure_resources:
            issues.append({
                "id": "mixed-content",
                "severity": "high",
                "category": "security",
                "message": "Recursos HTTP encontrados em uma página HTTPS.",
                "problem": f"Foram encontrados {len(insecure_resources)} recurso(s) carregado(s) por HTTP.",
                "recommendation": "Use HTTPS para os recursos carregados pela página.",
                "example": "https://exemplo.com/script.js"
            })
    
    
    # 46. Imagens sem width/height
    images_without_dimensions = []
    
    for image in soup.find_all("img"):
        if not image.get("width") or not image.get("height"):
            images_without_dimensions.append(image)
    
    if images_without_dimensions:
        issues.append({
            "id": "images-missing-dimensions",
            "severity": "low",
            "category": "performance",
            "message": f"{len(images_without_dimensions)} imagem(ns) sem dimensões definidas.",
            "problem": "Uma ou mais imagens não possuem width e height definidos.",
            "recommendation": "Defina as dimensões das imagens para ajudar a evitar mudanças inesperadas no layout.",
            "example": '<img src="imagem.jpg" width="800" height="600" alt="Descrição">'
        })
    
    
    # 47. Imagens potencialmente grandes
    large_image_candidates = []
    
    for image in soup.find_all("img"):
        src = image.get("src", "").strip()
    
        if src and any(
            extension in src.lower()
            for extension in [".png", ".jpg", ".jpeg", ".webp"]
        ):
            large_image_candidates.append(src)
    
    if len(large_image_candidates) > 20:
        issues.append({
            "id": "many-images",
            "severity": "low",
            "category": "performance",
            "message": "A página possui muitas imagens.",
            "problem": f"Foram encontradas {len(large_image_candidates)} imagens.",
            "recommendation": "Otimize, comprima e carregue imagens apenas quando necessário.",
            "example": '<img src="imagem.webp" loading="lazy" alt="Descrição">'
        })
    
    
    # 48. Iframes sem loading lazy
    iframes_without_lazy = []
    
    for iframe in soup.find_all("iframe"):
        if iframe.get("loading") != "lazy":
            iframes_without_lazy.append(iframe)
    
    if iframes_without_lazy:
        issues.append({
            "id": "iframe-without-lazy",
            "severity": "low",
            "category": "performance",
            "message": f"{len(iframes_without_lazy)} iframe(s) sem lazy loading.",
            "problem": "Iframes podem carregar recursos mesmo quando estão fora da área visível.",
            "recommendation": "Considere utilizar loading=\"lazy\" em iframes que não precisam carregar imediatamente.",
            "example": '<iframe src="mapa.html" loading="lazy" title="Mapa"></iframe>'
        })
    
    
    # 49. Vídeo sem preload adequado
    videos_without_preload = []
    
    for video in soup.find_all("video"):
        if not video.get("preload"):
            videos_without_preload.append(video)
    
    if videos_without_preload:
        issues.append({
            "id": "video-without-preload",
            "severity": "low",
            "category": "performance",
            "message": f"{len(videos_without_preload)} vídeo(s) sem preload definido.",
            "problem": "O comportamento de carregamento do vídeo não foi definido explicitamente.",
            "recommendation": "Defina preload de acordo com a necessidade do vídeo.",
            "example": '<video controls preload="metadata"></video>'
        })
    
    
    # 50. Áudio sem preload adequado
    audios_without_preload = []
    
    for audio in soup.find_all("audio"):
        if not audio.get("preload"):
            audios_without_preload.append(audio)
    
    if audios_without_preload:
        issues.append({
            "id": "audio-without-preload",
            "severity": "low",
            "category": "performance",
            "message": f"{len(audios_without_preload)} áudio(s) sem preload definido.",
            "problem": "O comportamento de carregamento do áudio não foi definido explicitamente.",
            "recommendation": "Defina preload de acordo com a necessidade do áudio.",
            "example": '<audio controls preload="metadata"></audio>'
        })
    
    
    return issues
