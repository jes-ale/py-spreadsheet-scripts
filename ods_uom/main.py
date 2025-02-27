
import os
import sys
import pandas as pd


def read_file(file_name):
    file_path = os.path.join(os.getcwd(), file_name)
    if os.path.exists(file_path):
        try:
            if file_name.endswith('.csv'):
                return pd.read_csv(file_path)
            elif file_name.endswith('.ods'):
                return pd.read_excel(file_path, engine='odf')
            else:
                print(f"Unsupported file format for '{file_name}'.")
                return None
        except Exception as e:
            print(f"Error reading file '{file_name}': {e}")
            return None
    else:
        print(f"File '{file_name}' not found in the current working directory.")
        return None


def crear_mapeo_categorias(categorias_df):
    """
    Crea un diccionario que mapea cada uom_external_id a su categoría.

    Args:
        categorias_df (pd.DataFrame): DataFrame con las categorías y sus unidades de medida.

    Returns:
        dict: Diccionario que mapea uom_external_id a su categoría.
    """
    categorias_df = categorias_df.ffill()  # Rellenar las categorías en las filas vacías
    uom_to_category = {}
    for _, row in categorias_df.iterrows():
        uom_to_category[row['uom_external_id']] = row['id']
    return uom_to_category


def validar_unidades_medida(productos_df, uom_to_category, col_unidad_compra, col_unidad_normal):
    """
    Valida que las unidades de medida de compra y normales de cada producto pertenezcan a la misma categoría.

    Args:
        productos_df (pd.DataFrame): DataFrame con los productos.
        uom_to_category (dict): Diccionario que mapea cada uom_external_id a su categoría.
        col_unidad_compra (str): Columna de la unidad de medida de compra.
        col_unidad_normal (str): Columna de la unidad de medida normal.

    Returns:
        pd.DataFrame: DataFrame con la columna de validación.
    """
    def validar_fila(row):
        categoria_compra = uom_to_category.get(row[col_unidad_compra])
        categoria_normal = uom_to_category.get(row[col_unidad_normal])
        return 1 if categoria_compra == categoria_normal else 0

    productos_df['validacion'] = productos_df.apply(validar_fila, axis=1)
    return productos_df


def main():
    """
    Función principal que maneja la validación de unidades de medida.
    """
    if len(sys.argv) < 5:
        print("Usage: python script.py <productos_file.ods/csv> <categorias_file.ods/csv> <unidad_compra_column> <unidad_normal_column>")
        sys.exit(1)

    productos_file_name = sys.argv[1]
    categorias_file_name = sys.argv[2]
    unidad_compra_column = sys.argv[3]
    unidad_normal_column = sys.argv[4]

    productos_df = read_file(productos_file_name)
    if productos_df is None:
        return

    categorias_df = read_file(categorias_file_name)
    if categorias_df is None:
        return

    # Crear mapeo de categorías
    uom_to_category = crear_mapeo_categorias(categorias_df)

    # Validar unidades de medida
    productos_df = validar_unidades_medida(productos_df, uom_to_category, unidad_compra_column, unidad_normal_column)

    # Guardar resultados en un archivo ODS
    output_file_name = 'productos_validados.csv'
    productos_df.to_csv(output_file_name, index=False)
    print(f"Validación completada. Archivo guardado como '{output_file_name}'.")


if __name__ == "__main__":
    main()
