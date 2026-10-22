#interfaz web con Streamlit

import streamlit as st
from analisis.procesamiento import validar_y_cargar_csv

# Configuración inicial de la página web
st.set_page_config(page_title="Minería de Datos - App", layout="wide")

st.title("Plataforma Web de Minería de Datos")
st.write("Sube tu archivo CSV para comenzar con la validación y limpieza automática.")

# Componente visual para subir archivos (S1)
uploaded_file = st.file_uploader("Elige un archivo CSV", type=["csv"])

if uploaded_file is not None:
    # Llamamos a nuestra función de validación que creamos en analisis/procesamiento.py
    df, error = validar_y_cargar_csv(uploaded_file)

    if error:
        st.error(error)
    else:
        st.success("¡Archivo CSV cargado y validado exitosamente!")

        # Mostrar una vista previa de las primeras filas (S1)
        st.subheader("Vista previa de los datos")
        st.dataframe(df.head(10))

        # Mostrar métricas rápidas del dataset
        st.info(f"Filas: {df.shape[0]} | Columnas: {df.shape[1]}")