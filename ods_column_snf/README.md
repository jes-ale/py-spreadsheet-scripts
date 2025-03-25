# ODS Cross-Reference Processor

This script performs intra-file cross-referencing in ODS spreadsheets, copying values between columns when specified relationships are found. Designed for data normalization tasks in inventory systems, CRM databases, and relational datasets.

---

## Features

- **Sheet-by-Sheet Processing**: Handles multi-sheet ODS files independently
- **Bidirectional Lookups**: Search values can be in different rows from target matches
- **Blank Handling**: Leaves non-matching cells empty by default
- **Data Integrity**: Preserves original file structure and formatting

---

## Requirements

- Python 3.6+
- Required Packages:
  ```bash
  pip install pandas ezodf
  ```

---

## Usage

### Command Syntax
```bash
python script.py <filename.ods> <search_column> <target_column> <output_column> <value_taken_column>
```

### Parameters
| Parameter | Description |
|-----------|-------------|
| `filename.ods` | Input ODS file |
| `search_column` | Column containing lookup values |
| `target_column` | Column to search for matches |
| `output_column` | Column to write results to |
| `value_taken_column` | Source column for matched values |

---

## Workflow

1. **Read Input File**: Loads all sheets from ODS file
2. **Row-by-Row Processing**:
   - Takes `search_column` value from current row
   - Finds first match in `target_column` across entire sheet
   - Copies `value_taken_column` from matching row to `output_column`
3. **Output Generation**: Creates separate files per sheet with `_processed_` suffix

---

## Example Scenario

### Input (data.ods)
**Products Sheet**
| ID | Related_ID | Supplier | Contact |
|----|------------|----------|---------|
| 101 | 205       | Acme     |         |
| 205 | 300       | Globex   | Jane    |

### Command
```bash
python script.py data.ods ID Related_ID Contact Supplier
```

### Output (data_processed_Products.ods)
| ID | Related_ID | Supplier | Contact |
|----|------------|----------|---------|
| 101 | 205       | Acme     | Jane    |
| 205 | 300       | Globex   |         |

---

## Key Notes

- **Case Sensitivity**: Matches are exact and case-sensitive
- **First Match Wins**: Uses first occurrence when multiple matches exist
- **Column Creation**: Creates `output_column` if non-existent
- **Performance**: Suitable for medium datasets (<100k rows)

---

## Error Handling

- **Missing Files**: Immediate exit with clear error
- **Invalid Columns**: Preserves original data with warning
- **Type Mismatches**: Attempts value conversion where possible

---

## License

[MIT License](LICENSE)
