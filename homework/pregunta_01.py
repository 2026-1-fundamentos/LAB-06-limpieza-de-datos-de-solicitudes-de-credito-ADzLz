"""
Escriba el codigo que ejecute la accion solicitada en la pregunta.
"""


def pregunta_01():
    """
    Realice la limpieza del archivo "files/input/solicitudes_de_credito.csv".
    El archivo tiene problemas como registros duplicados y datos faltantes.
    Tenga en cuenta todas las verificaciones discutidas en clase para
    realizar la limpieza de los datos.

    El archivo limpio debe escribirse en "files/output/solicitudes_de_credito.csv"

    """
    import glob
    import os
    import pandas as pd
    import unicodedata

    input_dir = "files/input"
    output_dir = "files/output"
    os.makedirs(output_dir, exist_ok=True)

    
    data = pd.read_csv(
        os.path.join(input_dir, "solicitudes_de_credito.csv"),
        sep=";",
        index_col=0,
    )

    # 2. Eliminar nulos iniciales de la base
    data.dropna(inplace=True)

    columnas_numericas = ["estrato", "comuna_ciudadano", "monto_del_credito"]
    columnas_texto = [
        "sexo",
        "tipo_de_emprendimiento",
        "idea_negocio",
        "barrio",
        "línea_credito",
    ]
    def eliminar_acentos(texto):
        texto = str(texto)
        # Convertir a formato Unicode descompuesto para separar letras de tildes
        texto = (
            unicodedata.normalize("NFKD", texto)
            .encode("ascii", "ignore")
            .decode("utf-8")
        )
        return texto
    # 3. Limpiar Columnas de Texto (Homogeneización estricta)
    for col in columnas_texto:
        if col in data.columns:
            data[col] = (
                data[col]
                .astype(str)
                .str.lower()
                .str.strip()
                .apply(eliminar_acentos)
                .str.replace("_", " ", regex=False)
                .str.replace("-", " ", regex=False)
                # CORRECCIÓN: Colapsar espacios múltiples internos en uno solo
                .str.replace(r"\s+", " ", regex=True)
                .str.strip()
            )

    # 4. Limpiar columna de fecha minuciosamente
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

    # 5. Limpiar Columnas Numéricas matemáticamente
    if "monto_del_credito" in data.columns:
        data["monto_del_credito"] = (
            data["monto_del_credito"]
            .astype(str)
            .str.strip()
            .str.replace("$", "", regex=False)
            .str.replace(",", "", regex=False)
            .str.strip()
        )

    # Convertir numéricos de manera segura con coerción nativa de tipos
    for col in columnas_numericas:
        if col in data.columns:
            data[col] = pd.to_numeric(data[col], errors="coerce")

    # 6. Eliminar nulos generados por la conversión y forzar enteros
    data.dropna(inplace=True)
    for col in columnas_numericas:
        data[col] = data[col].astype(int)

    # 7. Remover duplicados finales sobre la matriz completamente limpia
    data.drop_duplicates(inplace=True)
    for col in data.columns:

        print(f"Valores en {col}: {data[col].value_counts().to_list()}")

    # 8. Guardar el archivo limpio (index=False es obligatorio)
    output_file = os.path.join(output_dir, "solicitudes_de_credito.csv")
    data.to_csv(output_file, index=False, sep=";")
pregunta_01()