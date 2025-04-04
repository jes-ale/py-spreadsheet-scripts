# Python Scripts for Spreadsheet Manipulation

Este repositorio contiene scripts de Python diseñados para manipular hojas de cálculo en formatos CSV, ODS y XLSX. Estos scripts están destinados a ser ejecutados manualmente, requiriendo una cuidadosa atención a los detalles. Su objetivo es ayudar a los usuarios avanzados a encontrar ejemplos prácticos de scripts de Python para operaciones con hojas de cálculo.

A continuación, se detalla la metodología recomendada para ejecutar los scripts, así como la estructura del proyecto y los requisitos necesarios.

## Estructura del Proyecto

```
.
├── LICENSE
├── README.md
├── mx_zip_colony/
│   ├── README.md
│   ├── __init__.py
│   └── main.py
├── ods_batch/
│   ├── README.md
│   ├── __init__.py
│   └── main.py
├── ods_clear_values/
│   └── main.py
├── ods_column_snf/
│   └── main.py
├── ods_file_column_fnr/
│   └── main.py
├── ods_generate_externalID/
│   └── main.py
├── ods_uom/
│   └── main.py
└── requirements.txt
```

# Python 3.11 Virtual Environment Setup

## 1. Set Python 3.11 as local version
```bash
pyenv install 3.11.9  # Skip if already installed
pyenv local 3.11.9    # Sets for this directory only
```

## 2. Create and activate virtualenv
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate   # Windows
```

## 3. Install dependencies
```bash
pip install -r requirements.txt
```

## 4. Run your application
```bash
cd mx_zip_colony && python main.py
```

## Switching Back
```bash
pyenv local system  # Revert to system Python
deactivate         # Leave virtualenv
```
