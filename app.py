import streamlit as st
from analisis.procesamiento import validar_y_cargar_csv, limpiar_datos

# Configuración inicial de la página web
st.set_page_config(page_title="Minería de Datos - App", layout="wide")

st.title("Plataforma Web de Minería de Datos")
st.write("Sube tu archivo CSV para comenzar con la validación (S1) y limpieza automática (S2).")

# Componente visual para subir archivos (S1)
uploaded_file = st.file_uploader("Elige un archivo CSV", type=["csv"])

if uploaded_file is not None:
    # Llamamos a la función que retorna el DataFrame y el mensaje de error
    df, error = validar_y_cargar_csv(uploaded_file)
    
    if error is not None:
        st.error(error)
    else:
        st.success("¡Archivo CSV cargado y validado exitosamente!")
        
        # Vista previa de datos originales (S1)
        st.subheader("Vista previa de los datos originales (S1)")
        st.dataframe(df.head())

        # Botón para ejecutar la Limpieza Automática (S2)
        st.subheader("Limpieza Automática de Datos (S2)")
        if st.button("Ejecutar Limpieza Automática"):
            df_limpio = limpiar_datos(df)
            st.session_state['df_limpio'] = df_limpio
            st.success("¡Datos limpiados y normalizados correctamente!")

        # Mostrar resultado de la limpieza si ya fue realizada
        if 'df_limpio' in st.session_state:
            st.write("### Datos Limpios (S2)")
            st.dataframe(st.session_state['df_limpio'].head())