
import pandas as pd
import re
import ezodf
import os
import sys


def read_file(file_name):
    """
    Reads an ODS or CSV file and returns its contents as a dictionary.
    """
    file_path = os.path.join(os.getcwd(), file_name)
    if not os.path.exists(file_path):
        print(f"File '{file_name}' not found in the current working directory.")
        return None

    try:
        if file_name.endswith('.ods'):
            doc = ezodf.opendoc(file_path)
            ods_data = {}
            for sheet in doc.sheets:
                sheet_name = sheet.name
                data = []
                for row in sheet.rows():
                    row_data = []
                    for cell in row:
                        row_data.append(cell.value)
                    data.append(row_data)
                ods_data[sheet_name] = pd.DataFrame(data[1:], columns=data[0])
            return ods_data
        elif file_name.endswith('.csv'):
            df = pd.read_csv(file_path)
            return {"Sheet1": df}
        else:
            print(f"Unsupported file type for '{file_name}'. Only ODS and CSV files are supported.")
            return None
    except Exception as e:
        print(f"Error reading file '{file_name}': {e}")
        return None


def clean_values(value):
    """
    Limpia los valores para que solo contengan letras, números, _ y .
    """
    value = str(value)
    value = re.sub(r'\s+', '_', value)  # Reemplaza múltiples espacios con un solo _
    value = re.sub(r'[^a-zA-Z0-9_.]+', '', value)  # Elimina caracteres especiales excepto _, .
    value = value.lower()
    return value


def process_file(file_name, column_names, prefix=None, suffix=None):
    """
    Procesa el archivo ODS o CSV, selecciona las columnas indicadas y genera la columna "external_id".
    """
    data_dict = read_file(file_name)
    if data_dict is None:
        return

    for sheet_name, df in data_dict.items():
        df = generate_external_id(df, column_names, prefix, suffix)
        output_filename = f"{file_name}_processed_{sheet_name}.ods"
        output_path = os.path.join(os.getcwd(), output_filename)
        df_to_ods(df, output_path, sheet_name)
        print(f"Written {output_filename}")


def generate_external_id(df, column_names, prefix=None, suffix=None):
    """
    Genera una nueva columna llamada "external_id" a partir de los valores de las columnas seleccionadas.
    """
    # Asegurar que las columnas que deben ser enteros se mantengan como enteros
    for column in column_names:
        if pd.api.types.is_numeric_dtype(df[column]):
            df[column] = df[column].apply(lambda x: int(x) if pd.notna(x) and float(x).is_integer() else x)

    df[column_names] = df[column_names].apply(lambda x: x.apply(clean_values))
    external_id_values = df[column_names].apply(lambda row: '_'.join(str(x) for x in row), axis=1)
    if prefix:
        external_id_values = prefix + external_id_values
    if suffix:
        external_id_values = external_id_values + suffix
    df['external_id'] = external_id_values
    return df


def df_to_ods(df, file_path, sheet_name='Sheet1'):
    """
    Guarda un DataFrame en un archivo ODS, manteniendo el formato original de las columnas numéricas.
    """
    ods_doc = ezodf.newdoc(doctype="ods", filename=file_path)
    ods_sheet = ezodf.Sheet(sheet_name, size=(len(df) + 1, len(df.columns)))
    ods_doc.sheets += ods_sheet

    # Asegurar que las columnas que deben ser enteros se mantengan como enteros
    for column in df.columns:
        if pd.api.types.is_integer_dtype(df[column]):
            df[column] = df[column].astype(int)  # Convertir a int explícitamente

    for i, col in enumerate(df.columns):
        ods_sheet[0, i].set_value(col)  # Configurar el nombre de la columna en la primera fila

    for i, row in enumerate(df.itertuples(index=False, name=None), start=1):
        for j, value in enumerate(row):
            if value is None:
                ods_sheet[i, j].set_value("")  # Reemplaza None con una cadena vacía
            elif isinstance(value, int):
                ods_sheet[i, j].set_value(value)  # Escribe el valor como entero
            elif isinstance(value, float) and value.is_integer():
                ods_sheet[i, j].set_value(int(value))  # Convierte flotantes que son enteros a int
            else:
                ods_sheet[i, j].set_value(value)  # Mantén el valor original para otros tipos

    ods_doc.save()


def main():
    if len(sys.argv) < 3:
        print("Usage: python script.py <filename.ods/csv> <column1> [<column2> ...] [prefix] [suffix]")
        sys.exit(1)

    file_name = sys.argv[1]
    column_names = sys.argv[2:]
    prefix = None
    suffix = None

    for arg in column_names:
        if arg.startswith('-p='):
            prefix = arg[3:]
            column_names.remove(arg)
        elif arg.startswith('-s='):
            suffix = arg[3:]
            column_names.remove(arg)

    process_file(file_name, column_names, prefix, suffix)


if __name__ == "__main__":
    main()
