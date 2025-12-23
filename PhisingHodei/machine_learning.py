import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn import svm
from sklearn import tree
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt

# --- 1. CARGA Y PREPARACIÓN DE DATOS ---
try:
    legitimate_df = pd.read_csv('structured_data_legitimate.csv')
    phishing_df = pd.read_csv('structured_data_phishing.csv')
    
    # [cite_start]Unir ambos datasets y mezclar aleatoriamente [cite: 720-723]
    df = pd.concat([legitimate_df, phishing_df], axis=0)
    df = df.sample(frac=1).reset_index(drop=True)
    
    # [cite_start]Eliminar columna URL y duplicados [cite: 728-730]
    df = df.drop('URL', axis=1, errors='ignore')
    df = df.drop_duplicates()
    
    # [cite_start]Separar X (características) e Y (etiquetas) [cite: 732-733]
    X = df.drop('label', axis=1)
    Y = df['label']
    
    # [cite_start]Dividir en entrenamiento (80%) y prueba (20%) [cite: 738-744]
    x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=10)

except FileNotFoundError:
    print("ADVERTENCIA: No se encontraron los archivos CSV. Ejecuta data_collector.py primero.")
    # Variables vacías para evitar que la importación en app.py falle
    legitimate_df, phishing_df, df = pd.DataFrame(), pd.DataFrame(), pd.DataFrame()
    X, Y = pd.DataFrame(), pd.Series()
    x_train, x_test, y_train, y_test = None, None, None, None

# --- 2. DEFINICIÓN DE MODELOS ---
# [cite_start]Definimos los 7 modelos solicitados en el laboratorio [cite: 750]
svm_model = svm.LinearSVC(dual="auto")
rf_model = RandomForestClassifier(n_estimators=60)
dt_model = tree.DecisionTreeClassifier()
ab_model = AdaBoostClassifier() # 'SAMME' para evitar warnings en versiones nuevas
nb_model = GaussianNB()
nn_model = MLPClassifier(alpha=1, max_iter=1000)
kn_model = KNeighborsClassifier()

# --- 3. ENTRENAMIENTO Y EVALUACIÓN ---
# Diccionario para almacenar resultados
results = {'Accuracy': [], 'Precision': [], 'Recall': []}
models_list = [nb_model, svm_model, dt_model, rf_model, ab_model, nn_model, kn_model]
model_names = ['Naive Bayes', 'SVM', 'Decision Tree', 'Random Forest', 'AdaBoost', 'Neural Network', 'K-Neighbors']

# Solo ejecutamos el entrenamiento si hay datos cargados
if x_train is not None:
    print("Iniciando entrenamiento de modelos...")
    
    for model in models_list:
        try:
            # [cite_start]Entrenar [cite: 763]
            model.fit(x_train, y_train)
            
            # [cite_start]Predecir [cite: 765]
            predictions = model.predict(x_test)
            
            # [cite_start]Matriz de confusión [cite: 768]
            # Nota: Si el test set es muy pequeño o solo tiene una clase, puede dar error al desempaquetar. 
            # Usamos ravel() y lógica segura.
            tn, fp, fn, tp = confusion_matrix(y_true=y_test, y_pred=predictions, labels=[0,1]).ravel()
            
            # [cite_start]Métricas [cite: 776]
            accuracy = (tp + tn) / (tp + tn + fp + fn) if (tp + tn + fp + fn) > 0 else 0
            precision = tp / (tp + fp) if (tp + fp) > 0 else 0
            recall = tp / (tp + fn) if (tp + fn) > 0 else 0
            
            results['Accuracy'].append(accuracy)
            results['Precision'].append(precision)
            results['Recall'].append(recall)
            
        except Exception as e:
            print(f"Error entrenando modelo: {e}")
            results['Accuracy'].append(0)
            results['Precision'].append(0)
            results['Recall'].append(0)

    # [cite_start]Crear DataFrame de resultados [cite: 857]
    df_results = pd.DataFrame(data=results, index=model_names)

else:
    df_results = pd.DataFrame()

# --- 4. VISUALIZACIÓN ---
if __name__ == "__main__":
    print("\n--- Resultados del Entrenamiento ---")
    print(df_results)
    
    if not df_results.empty:
        ax = df_results.plot.bar(rot=0)
        plt.title("Comparativa de Modelos de Detección de Phishing")
        plt.show()