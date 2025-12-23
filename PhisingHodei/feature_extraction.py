from bs4 import BeautifulSoup
import os
import features # Importamos el archivo que acabas de crear
import pandas as pd

# 1. Función para abrir archivos (útil si pruebas con archivos descargados)
def open_file(file_name):
    with open(file_name, "r", encoding="utf-8") as f:
        return f.read()

# 2. Convertir texto a objeto BeautifulSoup
def create_soup(text):
    return BeautifulSoup(text, "html.parser")

# 3. CRUCIAL: Crear el vector de características
# Esta función toma un HTML (soup) y devuelve una lista de números [1, 0, 5, ...]
def create_vector(soup):
    vector = [
        # --- Binarias ---
        features.has_title(soup),
        features.has_input(soup),
        features.has_button(soup),
        features.has_image(soup),
        features.has_submit(soup),
        features.has_link(soup),
        features.has_password(soup),
        features.has_email_input(soup),
        features.has_hidden_element(soup),
        features.has_audio(soup),
        features.has_video(soup),
        
        # --- Cuantitativas ---
        features.number_of_inputs(soup),
        features.number_of_buttons(soup),
        features.number_of_images(soup),
        features.number_of_option(soup),
        features.number_of_list(soup),
        features.number_of_TH(soup),
        features.number_of_TR(soup),
        features.number_of_href(soup),
        features.number_of_paragraph(soup),
        features.number_of_script(soup),
        features.length_of_title(soup)
    ]
    return vector

# 4. Procesar una carpeta entera (para el mini_dataset)
def create_2d_list(folder_name):
    directory = os.path.join(os.getcwd(), folder_name)
    data = []
    # Itera sobre cada archivo en la carpeta
    for file in sorted(os.listdir(directory)):
        if file.endswith(".html"):
            try:
                soup = create_soup(open_file(os.path.join(directory, file)))
                vector = create_vector(soup)
                data.append(vector)
            except Exception as e:
                print(f"Error procesando {file}: {e}")
    return data