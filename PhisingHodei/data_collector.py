import pandas as pd
import requests as re
from bs4 import BeautifulSoup
import feature_extraction as fe
from urllib3.exceptions import InsecureRequestWarning
from urllib3 import disable_warnings

# Deshabilitar advertencias de certificados SSL (común en sitios de phishing)
disable_warnings(InsecureRequestWarning)

def normalize_url(url):
    # Asegura que la URL tenga el prefijo http o https
    if url.startswith("http://") or url.startswith("https://"):
        return url
    return "http://" + url

def create_structured_data(url_list):
    """Visita las URLs, extrae características y devuelve una lista de datos."""
    data_list = []
    
    for i in range(0, len(url_list)):
        try:
            # Petición con timeout corto (4s) para no bloquear el proceso
            response = re.get(url_list[i], verify=False, timeout=4)
            
            if response.status_code != 200:
                print(f"{i}. Error HTTP {response.status_code} en: {url_list[i]}")
            else:
                # Si la conexión es exitosa, extraemos características
                soup = BeautifulSoup(response.content, "html.parser")
                vector = fe.create_vector(soup)
                vector.append(str(url_list[i])) # Añadimos la URL al final para referencia
                data_list.append(vector)
                print(f"{i}. Éxito procesando: {url_list[i]}")
                
        except re.exceptions.RequestException as e:
            print(f"{i}. Fallo de conexión: {e}")
            continue
            
    return data_list

# --- BLOQUE PRINCIPAL DE EJECUCIÓN ---
if __name__ == "__main__":
    # Definimos los nombres de las columnas
    columns = [
        "has_title", "has_input", "has_button", "has_image", "has_submit", "has_link",
        "has_password", "has_email_input", "has_hidden_element", "has_audio", "has_video",
        "number_of_inputs", "number_of_buttons", "number_of_images", "number_of_option",
        "number_of_list", "number_of_th", "number_of_tr", "number_of_href",
        "number_of_paragraph", "number_of_script", "length_of_title", "URL", "label"
    ]

    # --- PASO 1: RECOLECTAR DATOS LEGÍTIMOS ---
    # Usamos una lista manual para asegurar que funcione rápido y bien
    print("\n--- Procesando Sitios Legítimos ---")
    legit_urls = [
        "https://www.google.com", "https://www.youtube.com", "https://www.wikipedia.org",
        "https://www.amazon.com", "https://www.facebook.com", "https://www.twitter.com",
        "https://www.instagram.com", "https://www.linkedin.com", "https://www.reddit.com",
        "https://www.netflix.com", "https://www.microsoft.com", "https://www.apple.com",
        "https://www.stackoverflow.com", "https://github.com", "https://www.python.org"
    ]
    legit_urls = [normalize_url(u) for u in legit_urls]
    
    legit_data = create_structured_data(legit_urls)
    
    df_legit = pd.DataFrame(data=legit_data, columns=columns[:-1])
    df_legit['label'] = 0 # 0 = Legítimo
    df_legit.to_csv("structured_data_legitimate.csv", index=False)
    print("✅ Guardado: structured_data_legitimate.csv")

    # --- PASO 2: RECOLECTAR DATOS PHISHING ---
    print("\n--- Procesando Sitios de Phishing ---")
    try:
        # Intentamos leer tu archivo verified_online.csv
        df_phish_raw = pd.read_csv("verified_online.csv")
        # Tomamos solo las primeras 50 para que no tarde horas
        phish_urls = df_phish_raw['url'].tolist()[0:50] 
        phish_urls = [normalize_url(u) for u in phish_urls]
        
        phish_data = create_structured_data(phish_urls)
        
        df_phish = pd.DataFrame(data=phish_data, columns=columns[:-1])
        df_phish['label'] = 1 # 1 = Phishing
        df_phish.to_csv("structured_data_phishing.csv", index=False)
        print("✅ Guardado: structured_data_phishing.csv")
    except FileNotFoundError:
        print("❌ No se encontró el archivo verified_online.csv")
    except Exception as e:
        print(f"❌ Error al procesar phishing: {e}")