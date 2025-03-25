# ODS Data Cleaner

A Python script for cleaning and converting specific columns in ODS files to CSV format with data type enforcement.

## Features
- Processes all sheets in an ODS file
- Performs column-specific cleaning operations:
  - Strip leading/trailing spaces
  - Remove single quotes
  - Handle missing values (replace with '0')
- Converts columns to integer or float data types
- Automatic duplicate removal
- Outputs cleaned data to CSV (one CSV per sheet)

## Requirements
- Python 3.6+
- Dependencies: `pandas`, `ezodf`

Install requirements:
```bash
pip install pandas ezodf
```

## Usage
```bash
python script.py <filename.ods>
```

### Interactive Prompts
1. **Column to clean**: Enter exact column name from your ODS file
2. **Data type**: Choose between `integer` or `float`
3. **Cleaning operations**: Select from:
   - `1`: Strip spaces
   - `2`: Remove quotes
   - `3`: Handle missing values

### Example Session
```bash
$ python script.py sales_data.ods
Enter the column name to clean: Price
Enter the data type (integer/float): float
Select cleaning operations (comma-separated):
1. Strip leading/trailing spaces
2. Remove unwanted characters (e.g., single quotes)
3. Handle missing values (replace with '0')
Enter your choices (e.g., 1,2,3) or press Enter to skip: 1,3

Processing sheet: Monthly_Sales
Cleaned file saved as sales_data_Monthly_Sales.csv
Processing sheet: Inventory
Cleaned file saved as sales_data_Inventory.csv
```

## Output
- Creates CSV files for each sheet in original ODS
- Naming convention: `[original_filename]_[sheet_name].csv`
- Preserves header row from original data
- Removes duplicate rows automatically

## Data Handling Rules
1. **Type Conversion**:
   - Invalid values become `NaN` in numeric columns
   - Original values preserved as strings if conversion fails
2. **Missing Values**:
   - Empty strings → Converted to '0' if selected
   - NaN values remain in float columns
3. **Error Handling**:
   - Skips non-existent columns with warning
   - Continues processing other sheets if errors occur

## Limitations
- Processes all sheets in input ODS file
- Only supports integer/float conversions
- CSV encoding defaults to UTF-8
- Requires exact column name match
