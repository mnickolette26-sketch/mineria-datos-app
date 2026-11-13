import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from analisis.procesamiento import (
    validar_y_cargar_csv, 
    limpiar_datos, 
    obtener_resumen_estadistico
)

# Configuración inicial de la página web
st.set_page_config(page_title="Minería de Datos - App", layout="wide")

st.title("Plataforma Web de Minería de Datos")
st.write("Carga de datos (S1), Limpieza automática (S2) y Análisis Exploratorio - EDA (S3).")

# Componente visual para subir archivos (S1)
uploaded_file = st.file_uploader("Elige un archivo CSV", type=["csv"])

if uploaded_file is not None:
    df, error = validar_y_cargar_csv(uploaded_file)
    
    if error is not None:
        st.error(error)
    else:
        st.success("¡Archivo CSV cargado y validado exitosamente!")
        
        # Vista previa de datos originales (S1)
        st.subheader("1. Datos originales (S1)")
        st.dataframe(df.head())

        # Botón para ejecutar la Limpieza Automática (S2)
        st.subheader("2. Limpieza Automática de Datos (S2)")
        if st.button("Ejecutar Limpieza Automática"):
            df_limpio = limpiar_datos(df)
            st.session_state['df_limpio'] = df_limpio
            st.success("¡Datos limpiados y normalizados correctamente!")

        # Mostrar resultado de la limpieza y habilitar la S3 si ya se limpió
        if 'df_limpio' in st.session_state:
            df_l = st.session_state['df_limpio']
            st.write("### Vista previa de Datos Limpios (S2)")
            st.dataframe(df_l.head())

            # SECCIÓN S3: Análisis Exploratorio de Datos (EDA)
            st.markdown("---")
            st.subheader("3. Análisis Exploratorio de Datos (S3 - EDA)")
            
            resumen_num, info_col = obtener_resumen_estadistico(df_l)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("#### Estructura y Tipos de Datos")
                st.dataframe(info_col)

            with col2:
                st.write("#### Resumen Estadístico (Numéricas)")
                st.dataframe(resumen_num)

            st.write("#### Visualizaciones")
            columnas_numericas = df_l.select_dtypes(include=['int64', 'float64']).columns
            
            if len(columnas_numericas) > 0:
                col_seleccionada = st.selectbox(
                    "Selecciona una columna numérica para graficar su distribución:", 
                    columnas_numericas
                )
                
                fig, ax = plt.subplots(figsize=(8, 4))
                sns.histplot(df_l[col_seleccionada], kde=True, ax=ax, color="skyblue")
                ax.set_title(f"Distribución de {col_seleccionada}")
                st.pyplot(fig)
            else:
                st.info("El dataset no contiene columnas numéricas para graficar distribuciones.")

                # SECCIÓN S3.2: Módulo de Árbol de Decisión 
        st.markdown("---")
        st.subheader("4. Módulo de Árbol de Decisión (RF3)")
        
        from sklearn.model_selection import train_test_split
        from sklearn.tree import DecisionTreeClassifier, plot_tree
        from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
        import pandas as pd

        columnas_disponibles = df_l.columns.tolist()
        
        col_t1, col_t2 = st.columns(2)
        with col_t1:
            variable_objetivo = st.selectbox("Selecciona la Variable Objetivo (y):", columnas_disponibles)
        with col_t2:
            variables_predictoras = st.multiselect("Selecciona las Variables Predictoras (X):", [c for c in columnas_disponibles if c != variable_objetivo])

        if variable_objetivo and variables_predictoras:
            # Parámetros del modelo
            max_depth = st.slider("Profundidad máxima del árbol (max_depth):", 1, 20, 5)
            test_size = st.slider("Proporción de prueba (Test Split):", 0.1, 0.5, 0.2)

            if st.button("Entrenar Árbol de Decisión"):
                try:
                    X = df_l[variables_predictoras]
                    y = df_l[variable_objetivo]
                    
                    # Codificar variables categóricas si las hay
                    X = pd.get_dummies(X, drop_first=True)
                    
                    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42)
                    
                    clf = DecisionTreeClassifier(max_depth=max_depth, random_state=42)
                    clf.fit(X_train, y_train)
                    
                    y_pred = clf.predict(X_test)
                    
                    # Métricas
                    acc = accuracy_score(y_test, y_pred)
                    
                    st.success(f"¡Modelo entrenado con éxito! Exactitud (Accuracy): {acc:.4f}")
                    
                    # Mostrar reporte de clasificación y matriz
                    st.write("#### Métricas de Evaluación")
                    st.text(classification_report(y_test, y_pred))
                    
                    # Visualización del árbol
                    st.write("#### Visualización del Árbol de Decisión")
                    fig_tree, ax_tree = plt.subplots(figsize=(12, 8))
                    plot_tree(clf, feature_names=list(X.columns), class_names=[str(c) for c in clf.classes_], filled=True, ax=ax_tree)
                    st.pyplot(fig_tree)
                    
                except Exception as e:
                    st.error(f"Error al entrenar el modelo: {e}")