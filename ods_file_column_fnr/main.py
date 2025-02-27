
import os
import sys
import pandas as pd


def read_file(file_name):
    file_path = os.path.join(os.getcwd(), file_name)
    if os.path.exists(file_path):
        try:
            if file_name.endswith('.csv'):
                df = pd.read_csv(file_path)
            elif file_name.endswith('.ods'):
                df = pd.read_excel(file_path, engine='odf')
            else:
                print(f"Unsupported file format for '{file_name}'.")
                return None
            return df
        except Exception as e:
            print(f"Error reading file '{file_name}': {e}")
            return None
    else:
        print(f"File '{file_name}' not found in the current working directory.")
        return None


def clean_int_values(value):
    """
    Cleans the value to ensure it's an integer if possible.
    """
    try:
        # Remove unwanted characters like quotes
        cleaned_value = str(value).replace("'", "").strip()
        # Convert to integer if possible
        return int(cleaned_value)
    except ValueError:
        # If conversion fails, return the original value
        return value


def main():
    if len(sys.argv) < 6:
        print("Usage: python script.py <input_file.ods/csv> <output_file.csv> <search_column> <taken_column> <target_column>")
        sys.exit(1)

    input_file_name = sys.argv[1]
    output_file_name = sys.argv[2]
    search_column = sys.argv[3]
    taken_column = sys.argv[4]
    target_column = sys.argv[5]

    input_df = read_file(input_file_name)
    if input_df is None:
        return

    output_df = read_file(output_file_name)
    if output_df is None:
        return

    # Create a mapping from search_column to taken_column
    print("Creating mapping from search_column to taken_column.")
    try:
        # Clean integer-like values in the columns
        input_df[search_column] = input_df[search_column].apply(clean_int_values)
        input_df[taken_column] = input_df[taken_column].apply(clean_int_values)

        mapping = input_df[[search_column, taken_column]].dropna().drop_duplicates().set_index(search_column)[taken_column].to_dict()
    except Exception as e:
        print(f"Error creating mapping: {e}")
        return

    # Update the target_column in output_df based on the mapping
    print(f"Updating '{target_column}' in output_df based on the mapping.")
    try:
        # Clean integer-like values in the target column
        output_df[target_column] = output_df[target_column].apply(clean_int_values)
        output_df[target_column] = output_df[target_column].map(mapping).fillna(output_df[target_column])
    except Exception as e:
        print(f"Error updating '{target_column}' column: {e}")
        return

    # Check and fix integer conversion issues
    if output_df[target_column].dtype == 'float64':
        print(f"Column '{target_column}' is of float type. Checking for integer conversion.")
        try:
            if output_df[target_column].dropna().apply(lambda x: x.is_integer() if pd.notna(x) else False).all():
                output_df[target_column] = output_df[target_column].astype('Int64')  # Convert to nullable integer type
                print(f"Successfully converted '{target_column}' to nullable integer type.")
            else:
                print(f"Column '{target_column}' contains non-integer values or NaNs. Values remain as floats.")
        except Exception as e:
            print(f"Error converting '{target_column}' to integer type: {e}")

    # Write the processed data to the output file
    try:
        output_df.to_csv(output_file_name, index=False)
        print(f"Written {output_file_name}")
    except Exception as e:
        print(f"Error writing file '{output_file_name}': {e}")


if __name__ == "__main__":
    main()
