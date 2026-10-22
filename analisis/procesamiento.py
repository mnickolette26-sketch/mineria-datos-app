#lógica de validación

import pandas as pd
import io

def validar_y_cargar_csv(uploaded_file):
    """
    Valida el formato del archivo y carga el CSV usando pandas.
    Retorna un DataFrame si es exitoso o un mensaje de error.
    """
    if uploaded_file is not None:
        # Validar extensión del archivo
        if not uploaded_file.name.endswith('.csv'):
            return None, "Error: El archivo debe tener formato .csv"

        try:
            # Intentar leer el CSV con pandas usando codificación utf-8
            df = pd.read_csv(uploaded_file, encoding='utf-8')

            # Validar que el archivo no esté vacío
            if df.empty:
                return None, "Error: El archivo CSV está vacío."

            return df, None
        except Exception as e:
            try:
                # Intento alternativo con codificación latin1 si falla utf-8
                uploaded_file.seek(0)
                df = pd.read_csv(uploaded_file, encoding='latin1')
                return df, None
            except Exception as err:
                return None, f"Error al leer el archivo: {str(err)}"

    return None, "No se ha subido ningún archivo."