# ODS File to Batches

A Python script to split large ODS files into smaller chunks while preserving data integrity.

## Features
- Splits ODS files by row count (default: 10,000 rows per file)
- Handles multiple sheets (creates separate file sets per sheet)
- Preserves headers and data types
- Converts large numbers (>1e+15) to strings to prevent precision loss

