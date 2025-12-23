from bs4 import BeautifulSoup

# --- CARACTERÍSTICAS BINARIAS (Sí/No) ---

def has_title(soup):
    # Verifica si existe etiqueta title y si tiene texto dentro [cite: 341-344]
    if soup.title and soup.title.text.strip():
        return 1
    return 0

def has_input(soup):
    # Busca si hay alguna etiqueta <input> [cite: 348-352]
    if len(soup.find_all("input")) > 0:
        return 1
    return 0

def has_button(soup):
    # Busca etiquetas <button> [cite: 357-361]
    if len(soup.find_all("button")) > 0:
        return 1
    return 0

def has_image(soup):
    # Busca etiquetas <image> (Nota: en HTML moderno suele ser <img>, pero seguimos el PDF) [cite: 362-366]
    if len(soup.find_all("image")) == 0:
        return 0
    return 1

def has_link(soup):
    # Busca etiquetas <link> [cite: 367-371]
    if len(soup.find_all("link")) > 0:
        return 1
    return 0

def has_submit(soup):
    # Busca inputs de tipo "submit", típicos de formularios de login [cite: 376-381]
    for button in soup.find_all("input"):
        if button.get("type") == "submit":
            return 1
    return 0

def has_password(soup):
    # Busca inputs relacionados con contraseñas por tipo, nombre o id [cite: 384-388]
    for input in soup.find_all("input"):
        if (input.get("type") or input.get("name") or input.get("id")) == "password":
            return 1
    return 0

def has_email_input(soup):
    # Busca inputs relacionados con emails [cite: 391-395]
    for input in soup.find_all("input"):
        if (input.get("type") or input.get("id") or input.get("name")) == "email":
            return 1
    return 0

def has_hidden_element(soup):
    # Detecta elementos ocultos, usados a veces para esconder datos maliciosos [cite: 399-403]
    for input in soup.find_all("input"):
        if input.get("type") == "hidden":
            return 1
    return 0

def has_audio(soup):
    # [cite: 406-410]
    if len(soup.find_all("audio")) > 0:
        return 1
    return 0

def has_video(soup):
    # [cite: 411-415]
    if len(soup.find_all("video")) > 0:
        return 1
    return 0

# --- CARACTERÍSTICAS CUANTITATIVAS (Conteo) ---

def number_of_inputs(soup):
    # Cuenta inputs totales [cite: 418-419]
    return len(soup.find_all("input"))

def number_of_buttons(soup):
    # Cuenta botones totales [cite: 422-423]
    return len(soup.find_all("button"))

def number_of_images(soup):
    # Cuenta etiquetas image Y metaetiquetas de tipo imagen [cite: 426-432]
    image_tags = len(soup.find_all("image"))
    count = 0
    for meta in soup.find_all("meta"):
        if meta.get("type") == "image" or meta.get("name") == "image":
            count += 1
    return image_tags + count

def number_of_option(soup):
    # [cite: 434-435]
    return len(soup.find_all("option"))

def number_of_list(soup):
    # [cite: 436-437]
    return len(soup.find_all("li"))

def number_of_TH(soup):
    # Encabezados de tabla [cite: 438-439]
    return len(soup.find_all("th"))

def number_of_TR(soup):
    # Filas de tabla [cite: 440-441]
    return len(soup.find_all("tr"))

def number_of_href(soup):
    # Cuenta enlaces con atributo href [cite: 443-448]
    count = 0
    for link in soup.find_all("link"):
        if link.get("href"):
            count += 1
    return count

def number_of_paragraph(soup):
    # [cite: 450-451]
    return len(soup.find_all("p"))

def number_of_script(soup):
    # [cite: 452-453]
    return len(soup.find_all("script"))

def length_of_title(soup):
    # Longitud del texto del título [cite: 455-458]
    if soup.title and soup.title.text:
        return len(soup.title.text.strip())
    return 0