# CSV/ODS Data Mapping Script

This script maps values from a column in an input file to a target column in an output file, with support for cleaning integer values and handling data type conversions. It is designed for scenarios where relational data needs to be synchronized between two datasets (e.g., updating IDs to human-readable names).

---

## Features

- **Multi-Format Support**: Processes both CSV and ODS files (input/output).
- **Value Mapping**: Uses a mapping from the input file to update values in the output file.
- **Integer Cleaning**: Removes quotes and attempts to convert values to integers where possible.
- **Type Conversion**: Automatically converts float columns to nullable integer types if applicable.
- **Error Resilience**: Handles file read/write errors and provides detailed feedback.

---

## Prerequisites

- **Python 3.x**
- Required Libraries:
  - `pandas`: For data manipulation.
  - `odfpy` (for ODS support): Required only if processing ODS files.
  
  Install dependencies using:
  ```bash
  pip install pandas odfpy
  ```

---

## Usage

### Command Syntax
```bash
python script.py <input_file> <output_file> <search_column> <taken_column> <target_column>
```

### Parameters
| Parameter           | Description                                                                 |
|---------------------|-----------------------------------------------------------------------------|
| `input_file`        | Input file (CSV/ODS) containing the mapping data (`search_column` → `taken_column`). |
| `output_file`       | **Existing** output file (CSV/ODS) to update. The `target_column` in this file will be modified. |
| `search_column`     | Column in `input_file` to use as the lookup key.                            |
| `taken_column`      | Column in `input_file` to copy values from when a match is found.           |
| `target_column`     | Column in `output_file` to update with mapped values.                      |

### Example
```bash
python script.py customers.ods orders.csv CustomerID CustomerName OrderCustomer
```
- **Input File (`customers.ods`)**: Maps `CustomerID` (search) to `CustomerName` (taken).
- **Output File (`orders.csv`)**: Updates the `OrderCustomer` column (target) with names from `customers.ods` based on matching `CustomerID`.

---

## Workflow

1. **Read Input File**: Loads `input_file` (CSV/ODS) to create a `search_column` → `taken_column` mapping.
2. **Clean Values**:
   - Removes quotes from values (e.g., `'123'` → `123`).
   - Attempts to convert `search_column` and `taken_column` to integers where possible.
3. **Update Output File**:
   - Loads `output_file` (must exist).
   - Maps values in its `target_column` using the input file's data.
   - Preserves original values if no match is found.
4. **Type Conversion**:
   - Converts `target_column` to nullable integers if all values are integers or `NaN`.
5. **Save Results**: Overwrites `output_file` with updated data.

---

## Output

- The `output_file` is modified in-place with updated values in the `target_column`.
- **Note**: The script overwrites the original `output_file`. Ensure you have a backup if needed.

---

## Notes

- **Integer Cleaning**: Non-integer values (e.g., `"ABC"`) are left unchanged.
- **Case Sensitivity**: Matching is case-sensitive.
- **Column Headers**: Both files must have headers matching the specified column names.
- **ODS Support**: Requires `odfpy` for ODS file processing.

---

## Error Handling

- **Missing Files**: Terminates if `input_file` or `output_file` is not found.
- **Invalid Columns**: Fails gracefully if specified columns are missing in either file.
- **Type Conversion Warnings**: Alerts if `target_column` cannot be converted to integers.

---

## Example Scenario

### Input File (`customers.ods`)
| CustomerID | CustomerName |
|------------|--------------|
| 101        | Alice        |
| 102        | Bob          |

### Output File (`orders.csv`) Before
| OrderID | OrderCustomer |
|---------|---------------|
| 101     | '101'         |
| 103     | '103'         |

### Command
```bash
python script.py customers.ods orders.csv CustomerID CustomerName OrderCustomer
```

### Output File (`orders.csv`) After
| OrderID | OrderCustomer |
|---------|---------------|
| 101     | Alice         |
| 103     | 103           |

---

## License

This script is provided under the [MIT License](LICENSE).
