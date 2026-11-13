import pandas as pd
import io

def validar_y_cargar_csv(uploaded_file):
    """
    Valida el formato del archivo y carga el CSV usando pandas detectando el separador.
    """
    if uploaded_file is not None:
        if not uploaded_file.name.endswith('.csv'):
            return None, "Error: El archivo debe tener formato .csv"

        try:
            # Lectura con separador autodetectado y utf-8
            df = pd.read_csv(uploaded_file, encoding='utf-8', sep=None, engine='python')

            if df.empty:
                return None, "Error: El archivo CSV está vacío."

            return df, None
        except Exception as e:
            try:
                # Lectura alternativa con latin1
                uploaded_file.seek(0)
                df = pd.read_csv(uploaded_file, encoding='latin1', sep=None, engine='python')
                
                if df.empty:
                    return None, "Error: El archivo CSV está vacío."
                
                return df, None
            except Exception as err:
                return None, f"Error al leer el archivo: {str(err)}"

    return None, "No se ha subido ningún archivo."

def limpiar_datos(df):
    """
    Función para ejecutar la limpieza automática de datos (S2).
    """
    df_limpio = df.copy()

    # 1. Eliminar filas completamente duplicadas
    df_limpio = df_limpio.drop_duplicates()

    # 2. Limpieza de texto: Eliminar espacios en blanco adicionales
    columnas_texto = df_limpio.select_dtypes(include=['object']).columns
    for col in columnas_texto:
        df_limpio[col] = df_limpio[col].astype(str).str.strip()

    # 3. Tratamiento de valores nulos
    for col in df_limpio.columns:
        if df_limpio[col].dtype in ['int64', 'float64']:
            mediana = df_limpio[col].median()
            df_limpio[col] = df_limpio[col].fillna(mediana)
        else:
            df_limpio[col] = df_limpio[col].fillna('Desconocido')

    return df_limpio

def obtener_resumen_estadistico(df):
    """
    Calcula resumen estadístico e información de columnas para el EDA (S3).
    """
    resumen_numerico = df.describe()
    info_columnas = pd.DataFrame({
        'Tipo de Dato': df.dtypes.astype(str),
        'Valores Nulos': df.isnull().sum(),
        'Valores Únicos': df.nunique()
    })
    return resumen_numerico, info_columnas