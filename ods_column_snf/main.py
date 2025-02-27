import re
import pandas as pd
import ezodf
import os
import sys


def read_file(file_name):
    """
    Reads an ODS file and returns its contents as a dictionary.
    """
    file_path = os.path.join(os.getcwd(), file_name)
    if os.path.exists(file_path):
        try:
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
        except Exception as e:
            print(f"Error reading ODS file '{file_name}': {e}")
            return None
    else:
        print(f"File '{file_name}' not found in the current working directory.")
        return None


def process_ods(file_name, search_column, target_column, output_column, value_taken_column):
    """
    Procesa el archivo ODS, busca el valor en la columna de búsqueda en toda la tabla,
    y cuando lo encuentra, escribe el valor de la columna objetivo en la columna de salida.
    """
    data_dict = read_file(file_name)
    if data_dict is None:
        return

    for sheet_name, df in data_dict.items():
        df = search_and_write(df, search_column, target_column, output_column, value_taken_column)
        output_filename = f"{file_name}_processed_{sheet_name}.ods"
        output_path = os.path.join(os.getcwd(), output_filename)
        df.to_excel(output_path, index=False)
        print(f"Written {output_filename}")


def search_and_write(df, search_column, target_column, output_column, value_taken_column):
    """
    Busca el valor en la columna de búsqueda en toda la tabla,
    y cuando lo encuentra, escribe el valor de la columna objetivo en la columna de salida.
    """
    for index, row in df.iterrows():
        search_value = row[search_column]
        # Busca en el resto de los registros para encontrar una coincidencia
        matching_row = df[df[target_column] == search_value]
        if not matching_row.empty:
            # Extrae el valor de la columna indicada como value_taken_column
            taken_value = matching_row[value_taken_column].values[0]
            df.at[index, output_column] = taken_value
        else:
            # Si no se encuentra una coincidencia, se puede dejar en blanco o establecer un valor por defecto
            df.at[index, output_column] = None
    return df


def main():
    if len(sys.argv) < 5:
        print("Usage: python script.py <filename.ods> <search_column> <target_column> <output_column> <value_taken_column>")
        sys.exit(1)

    file_name = sys.argv[1]
    search_column = sys.argv[2]
    target_column = sys.argv[3]
    output_column = sys.argv[4]
    value_taken_column = sys.argv[5]

    process_ods(file_name, search_column, target_column, output_column, value_taken_column)


if __name__ == "__main__":
    main()
    # python script.py input.ods search_column target_column output_column value_taken_column
