"""
Escriba el codigo que ejecute la accion solicitada en la pregunta.
"""


import glob
import os
import pandas as pd
import unicodedata


def pregunta_01():
    input_dir = "files/input"
    output_dir = "files/output"
    os.makedirs(output_dir, exist_ok=True)

    data = pd.read_csv(
        os.path.join(input_dir, "solicitudes_de_credito.csv"),
        sep=";",
        index_col=0,
    )

    # 2. Eliminar nulos iniciales
    data.dropna(inplace=True)

    columnas_numericas = ["estrato", "comuna_ciudadano", "monto_del_credito"]
    columnas_texto = [
        "sexo",
        "tipo_de_emprendimiento",
        "idea_negocio",
        "barrio",
        "línea_credito",
    ]

    # Función para remover tildes/acentos de forma segura
    def eliminar_acentos(texto):
        if pd.isna(texto):
            return texto
        texto = str(texto)
        return (
            unicodedata.normalize("NFKD", texto)
            .encode("ascii", "ignore")
            .decode("utf-8")
        )

    # 3. Limpieza de columnas de texto
    for col in columnas_texto:
        if col in data.columns:
            if col == "barrio":
                # Limpieza para BARRIO (SIN eliminar acentos/tildes ni eñes)
                data[col] = (
                    data[col]
                    .astype(str)
                    .str.lower()
                    # Corregir los caracteres corruptos manteniendo la eñe y la tilde originales
                    .str.replace("antonio nari¿o", "antonio nariño", regex=False)
                    .str.replace("bel¿n", "belén", regex=False)
                    # Unificar guiones por espacios (el punto NO se toca)
                    .str.replace("_", " ", regex=False)
                    .str.replace("-", " ", regex=False)
                    # Colapsar espacios múltiples intermedios
                    .str.replace(r"\s+", " ", regex=True)
                    .str.strip()
                )
            else:
                # Limpieza estándar para las demás columnas de texto (CON eliminación de acentos)
                data[col] = (
                    data[col]
                    .astype(str)
                    .str.lower()
                    # Unificar guiones por espacios
                    .str.replace("_", " ", regex=False)
                    .str.replace("-", " ", regex=False)
                    # Colapsar espacios múltiples intermedios
                    .str.replace(r"\s+", " ", regex=True)
                    .str.strip()
                )
    # 4. Homogeneizar fechas a formato YYYY-MM-DD
    if "fecha_de_beneficio" in data.columns:

        def limpiar_fecha(x):
            parts = str(x).strip().split("/")
            if len(parts) == 3:
                if len(parts[0]) == 4:  # YYYY/MM/DD
                    return f"{parts[0]}-{parts[1].zfill(2)}-{parts[2].zfill(2)}"
                if len(parts[2]) == 4:  # DD/MM/YYYY
                    return f"{parts[2]}-{parts[1].zfill(2)}-{parts[0].zfill(2)}"
            return x

        data["fecha_de_beneficio"] = data["fecha_de_beneficio"].apply(
            limpiar_fecha
        )

    # 5. Estandarizar la columna de montos
    if "monto_del_credito" in data.columns:
        data["monto_del_credito"] = (
            data["monto_del_credito"]
            .astype(str)
            .str.strip()
            .str.replace("$", "", regex=False)
            .str.replace(",", "", regex=False)
            .str.replace(".00", "", regex=False)
            .str.replace(".0", "", regex=False)
            .str.strip()
        )

    # Convertir numéricos de forma nativa unificando formatos como "02" o "2.0"
    for col in columnas_numericas:
        if col in data.columns:
            data[col] = pd.to_numeric(data[col], errors="coerce")

    # 6. Eliminar nulos que se hayan generado en la conversión y pasar a enteros
    data.dropna(inplace=True)
    for col in columnas_numericas:
        data[col] = data[col].astype(int)

    # 7. Remover registros duplicados sobre la matriz limpia
    data.drop_duplicates(inplace=True)


    for col in data.columns:
        print(f'{col}: {data[col].value_counts().to_list()}')
    # 8. Guardar el archivo limpio sin el índice de pandas
    output_file = os.path.join(output_dir, "solicitudes_de_credito.csv")
    data.to_csv(output_file, index=False, sep=";")
    data["barrio"].value_counts().to_csv(os.path.join(output_dir, "barrio_counts.csv"), header=False, sep=";")
pregunta_01()