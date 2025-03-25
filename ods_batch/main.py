
import pandas as pd
import os
import sys
from pyexcel_ods3 import save_data
import ezodf


def read_file(file_name):
    """
    Reads an ODS file and returns its contents as a dictionary of DataFrames.

    Processes each sheet in the ODS file, converting rows into DataFrames. Replaces `None`
    values with empty strings to maintain data integrity. Handles file not found and read errors.

    Args:
        file_name (str): Name of the ODS file to read.

    Returns:
        dict: Keys are sheet names (str), values are pandas DataFrames. Returns None if the file
        is not found or an error occurs during reading.
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
                        row_data.append(cell.value if cell.value is not None else '')  # Replacing None with empty string
                    data.append(row_data)
                ods_data[sheet_name] = pd.DataFrame(data[1:], columns=data[0])
            return ods_data
        except Exception as e:
            print(f"Error reading ODS file '{file_name}': {e}")
            return None
    else:
        print(f"File '{file_name}' not found in the current working directory.")
        return None


def write_ods(data, output_path, sheet_name):
    """
    Writes a DataFrame to an ODS file, converting large numbers to strings to prevent precision loss.

    Overwrites existing files without warning. Converts values over 1e+15 to strings to avoid
    Excel/ODS precision limitations. Creates a single-sheet ODS file with the specified name.

    Args:
        data (pd.DataFrame): Data to write to the file.
        output_path (str): Full path for the output ODS file.
        sheet_name (str): Name of the sheet to create in the ODS file.
    """
    # Remove the existing file if it exists
    if os.path.exists(output_path):
        os.remove(output_path)

    # Convert large numbers to strings
    def convert_large_numbers(value):
        if isinstance(value, (int, float)):
            try:
                # Check if the number is too large
                if abs(value) > 1e+15:
                    return str(value)
            except Exception:
                return str(value)
        return value

    # Apply the conversion function to the DataFrame
    converted_df = data.applymap(convert_large_numbers)

    # Convert data to a dictionary suitable for saving
    sheet_data = {sheet_name: [list(converted_df.columns)] + converted_df.to_records(index=False).tolist()}

    # Save the data to an ODS file
    save_data(output_path, sheet_data)


def split_ods(file_name, max_rows=10000):
    """
    Splits an ODS file into multiple smaller ODS files based on row count.

    Processes each sheet separately, creating multiple files per sheet when needed. Output files
    are named with the original filename, sheet name, and a numerical suffix. Each output file
    contains up to `max_rows` rows of data (header row excluded from count).

    Args:
        file_name (str): Path to the input ODS file.
        max_rows (int, optional): Maximum rows per output file. Defaults to 10000.
    """
    # Read the ODS file
    data_dict = read_file(file_name)
    if data_dict is None:
        return

    base_filename, _ = os.path.splitext(file_name)

    # Iterate over each sheet in the dictionary
    for sheet_name, df in data_dict.items():
        num_rows = df.shape[0]
        num_files = (num_rows // max_rows) + (1 if num_rows % max_rows != 0 else 0)

        for i in range(num_files):
            start_row = i * max_rows
            end_row = start_row + max_rows
            # Slice the DataFrame
            slice_df = df.iloc[start_row:end_row]
            # Create a new filename for each slice
            output_filename = f"{base_filename}_{sheet_name}_{i + 1}.ods"
            output_path = os.path.join(os.getcwd(), output_filename)
            # Write the slice to a new ODS file
            write_ods(slice_df, output_path, sheet_name)
            print(f"Written {output_filename}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <filename.ods>")
        sys.exit(1)

    file_name = sys.argv[1]
    split_ods(file_name)
