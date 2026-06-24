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

    input_dir = "files/input"
    output_dir = "files/output"
    os.makedirs(output_dir, exist_ok=True)

    
    data = pd.read_csv(os.path.join(input_dir, "solicitudes_de_credito.csv"),sep=";", index_col=0)

    columnas_numericas = ['estrato','comuna_ciudadano','monto_del_credito']
    columnas_fechas = ["fecha_de_beneficio", "fecha_registro"]
    columnas_texto = ["sexo", 'tipo_de_emprendimiento', 'idea_negocio', 'barrio','línea_credito']

    # for col in columnas_numericas:
    #     valores_invalidos= []
    #     valores_invalidos = data[pd.to_numeric(data[col], errors='coerce').isna()][col].unique().tolist()

    #     print(f"Valores extraños detectados en {col}: {valores_invalidos}")
    for col in columnas_numericas:
        if col in data.columns:
            if col == "monto_del_credito":
                data[col] = (data[col].str.lower().str.strip()
                                .str.replace("$ ", "", regex=False)
                                .str.replace(".00", "", regex=False)
                                .str.replace(",", "", regex=False)
                                .str.replace(".", "", regex=False))
            data[col] = pd.to_numeric(data[col]).astype("Int64", errors='ignore')

    # for col in columnas_numericas:
    #     valores_invalidos= []
    #     valores_invalidos = data[pd.to_numeric(data[col], errors='coerce').isna()][col].unique().tolist()

    #     print(f"Valores extraños detectados en {col}: {valores_invalidos}")


    for col in columnas_fechas:
        if col in data.columns:
            data[col] = pd.to_datetime(data[col], errors='coerce', format='mixed')

    for col in columnas_texto:
        if col in data.columns:
            data[col] = (data[col].str.lower().str.strip()
                            .str.replace("_", " ", regex=False)
                            .str.replace("-", " ", regex=False))
            data[col] = data[col].replace(["nan", "none", "null", "unknown", ""], pd.NA)


    data["línea_credito"] = (data["línea_credito"].str.lower().str.strip()
                             .str.replace("_", " ", regex=False)
                             .str.replace("-", " ", regex=False))

    data = data.drop_duplicates()
    data = data.dropna()



    df = pd.DataFrame(data)
    output_file = os.path.join(output_dir, "solicitudes_de_credito.csv")
    df.to_csv(output_file, index=False)
