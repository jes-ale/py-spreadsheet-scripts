
import pandas as pd
import ezodf
import os
import sys


def clean_column(df, column, data_type, cleaning_ops):
    """
    Clean and convert values in the specified column based on the desired data type and cleaning operations.
    """
    if column in df.columns:
        # Copy original values if no cleaning operations are requested
        if not cleaning_ops:
            return df

        # Strip leading and trailing spaces if requested
        if 'strip_spaces' in cleaning_ops:
            df[column] = df[column].astype(str).str.strip()

        # Remove unwanted characters if requested
        if 'remove_quotes' in cleaning_ops:
            df[column] = df[column].str.replace("'", "", regex=False)  # Example of unwanted character removal

        # Handle missing values if requested
        if 'handle_missing' in cleaning_ops:
            df[column] = df[column].replace('', pd.NA)  # Replace empty strings with NaN
            df[column] = df[column].fillna('0')  # Replace NaN with '0'

        # Convert to the specified data type
        if data_type == 'integer':
            df[column] = pd.to_numeric(df[column], errors='coerce', downcast='integer')  # Convert to integer
        elif data_type == 'float':
            df[column] = pd.to_numeric(df[column], errors='coerce', downcast='float')  # Convert to float
        else:
            print(f"Unsupported data type: {data_type}. Column '{column}' will remain as string.")
            df[column] = df[column].astype(str)
    return df


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
                        try:
                            # Ensure cell values are treated as strings
                            if isinstance(cell.value, (str, int, float)):
                                cell_value = str(cell.value)
                            else:
                                cell_value = None  # Ignore non-string, non-numeric cells
                            row_data.append(cell_value)
                        except Exception as e:
                            print(f"Error processing cell: {e}")
                            row_data.append(None)  # Handle cell processing errors
                    data.append(row_data)
                ods_data[sheet_name] = pd.DataFrame(data[1:], columns=data[0])
            return ods_data
        except Exception as e:
            print(f"Error reading ODS file '{file_name}': {e}")
            return None
    else:
        print(f"File '{file_name}' not found in the current working directory.")
        return None


def save_to_csv(df, file_name):
    """
    Save the DataFrame to a CSV file.
    """
    output_filename = f"{file_name.replace('.ods', '.csv')}"
    output_path = os.path.join(os.getcwd(), output_filename)

    # Save DataFrame to CSV
    df.to_csv(output_path, index=False)
    print(f"Cleaned file saved as {output_filename}")


def process_file(file_name, column, data_type, cleaning_ops):
    """
    Process the ODS file to clean and convert the specified column's values.
    """
    data_dict = read_file(file_name)
    if data_dict is None:
        return

    for sheet_name, df in data_dict.items():
        try:
            # Remove duplicates
            df = df.drop_duplicates()

            # Clean and convert the specified column
            df = clean_column(df, column, data_type, cleaning_ops)

            # Save the cleaned DataFrame to CSV
            save_to_csv(df, file_name)
        except Exception as e:
            print(f"An error occurred while processing sheet '{sheet_name}': {e}")


def main():
    if len(sys.argv) < 2:
        print("Usage: python script.py <filename.ods>")
        sys.exit(1)

    file_name = sys.argv[1]

    # Get column name and data type
    column_name = input("Enter the column name to clean: ")
    data_type = input("Enter the data type (integer/float): ").lower()

    if data_type not in ['integer', 'float']:
        print(f"Unsupported data type: {data_type}. Use 'integer' or 'float'.")
        sys.exit(1)

    # Ask user for cleaning operations
    print("Select cleaning operations (comma-separated):")
    print("1. Strip leading/trailing spaces")
    print("2. Remove unwanted characters (e.g., single quotes)")
    print("3. Handle missing values (replace with '0')")
    ops_input = input("Enter your choices (e.g., 1,2,3) or press Enter to skip: ").strip()

    cleaning_ops = set()
    if '1' in ops_input:
        cleaning_ops.add('strip_spaces')
    if '2' in ops_input:
        cleaning_ops.add('remove_quotes')
    if '3' in ops_input:
        cleaning_ops.add('handle_missing')

    process_file(file_name, column_name, data_type, cleaning_ops)


if __name__ == "__main__":
    main()
