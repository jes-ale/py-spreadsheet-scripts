# CSV/ODS External ID Generator

This script processes CSV/ODS files to generate standardized `external_id` values by combining specified columns. It cleans input values, handles numeric formatting, and supports prefix/suffix additions. Ideal for creating unique identifiers from multi-column data.

---

## Features

- **Multi-Format Support**: Processes both CSV and multi-sheet ODS files
- **Value Cleaning**: Normalizes text to lowercase with underscores
- **Numeric Handling**: Maintains integer formatting for numeric columns
- **Flexible ID Creation**: Supports prefixes/suffixes for external IDs
- **Sheet Preservation**: Maintains original ODS sheet structure

---

## Prerequisites

- Python 3.8+
- Required packages:
  ```bash
  pip install pandas ezodf
  ```

---

## Usage

### Basic Command
```bash
python script.py <input_file> <column1> [column2...] [-p=PREFIX] [-s=SUFFIX]
```

### Parameters
| Parameter          | Description                                  |
|--------------------|----------------------------------------------|
| `input_file`       | Input CSV/ODS file                           |
| `column1`...       | Columns to combine for external_id           |
| `-p=PREFIX`        | Optional prefix for external_id              |
| `-s=SUFFIX`        | Optional suffix for external_id              |

### Examples
1. **Basic Usage**:
   ```bash
   python script.py data.ods product_id category
   ```
   - Creates `data.ods_processed_[sheetname].ods` with `external_id` column

2. **With Prefix/Suffix**:
   ```bash
   python script.py input.csv sku -p=prod_ -s=_2023
   ```
   - Generates IDs like `prod_abc123_2023`

---

## Value Cleaning Rules

1. Converts to lowercase
2. Replaces spaces with single underscores
3. Removes special characters (keeps only `a-z`, `0-9`, `_`, `.`)
4. Preserves numeric types
   - `123.0` → `123`
   - `'45.6'` → `45.6`

---

## Output Format

- Creates new ODS files for each input sheet
- Output filename pattern: `<input>_processed_<sheet>.ods`
- Maintains original columns + new `external_id` column

---

## Processing Workflow

1. **Read Input**: Supports both CSV and multi-sheet ODS
2. **Clean Columns**:
   ```python
   "Product Name" → "product_name"
   "ABC-123!" → "abc123"
   ```
3. **Generate IDs**:
   ```python
   columns = ["id", "category"]
   values = [101, "electronics"]
   → "101_electronics"
   ```
4. **Save Output**: Preserves original data types

---

## Error Handling

- **File Not Found**: Immediate termination with error message
- **Invalid Columns**: Skips missing columns
- **Type Errors**: Preserves original values with warnings

---

## Example Transformation

### Input (`data.ods`)
| product_id | Category    |
|------------|-------------|
| P-123      | Electronics |
| 456        | 'Furniture' |

### Command
```bash
python script.py data.ods product_id category -p=prod_
```

### Output (`data.ods_processed_Sheet1.ods`)
| product_id | Category    | external_id          |
|------------|-------------|----------------------|
| P-123      | Electronics | prod_p123_electronics|
| 456        | Furniture   | prod_456_furniture   |

---

## License
[MIT License](LICENSE)
