import streamlit as st
import machine_learning as ml
import feature_extraction as fe
from bs4 import BeautifulSoup
import requests as re
import matplotlib.pyplot as plt

# Configuración básica
st.set_page_config(page_title="Detector de Phishing", layout="wide")
st.title('🕵️ Detector de Phishing con IA')

# --- BARRA LATERAL ---
with st.sidebar:
    st.header("Estado del Sistema")
    if ml.x_train is not None:
        st.success("✅ Modelos Entrenados")
        st.write(f"Datos de entrenamiento: {len(ml.x_train)} sitios")
    else:
        st.error("⚠️ No hay datos cargados")

# --- SECCIÓN 1: RESULTADOS ---
st.header("1. Comparativa de Modelos")
st.write("Rendimiento de los 7 algoritmos entrenados:")
if not ml.df_results.empty:
    st.dataframe(ml.df_results.style.highlight_max(axis=0))
    st.bar_chart(ml.df_results['Accuracy'])
else:
    st.warning("Ejecuta data_collector.py primero para generar datos.")

# --- SECCIÓN 2: PRUEBA EN VIVO ---
st.header("2. Analizar una URL")
url = st.text_input("Pega aquí una URL sospechosa:", "https://www.google.com")

# Selector de modelo
model_name = st.selectbox("Elige el algoritmo:", ['Random Forest', 'SVM', 'Decision Tree', 'K-Neighbors'])
model_map = {
    'Random Forest': ml.rf_model,
    'SVM': ml.svm_model,
    'Decision Tree': ml.dt_model,
    'K-Neighbors': ml.kn_model
}

if st.button("🔍 Analizar"):
    try:
        with st.spinner("Escaneando contenido HTML..."):
            response = re.get(url, verify=False, timeout=5)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, "html.parser")
                vector = fe.create_vector(soup)
                
                # Predecir
                model = model_map[model_name]
                prediction = model.predict([vector])[0]
                
                if prediction == 0:
                    st.success("✅ SITIO LEGÍTIMO")
                else:
                    st.error("🚨 ¡PELIGRO! POSIBLE PHISHING")
            else:
                st.error("No se pudo conectar a la web.")
    except Exception as e:
        st.error(f"Error: {e}")