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

## Metodología para Ejecutar los Scripts

1. **Requisitos Previos**: Asegúrate de tener Python 3 instalado en tu sistema. Puedes verificar la versión de Python ejecutando:
   ```bash
   python3 --version
   ```

2. **Instalación de Dependencias**:
   - **Crear un entorno virtual** (opcional pero recomendado):
     ```bash
     python -m venv venv
     ```
   - **Activar el entorno virtual**:
     - En Windows:
       ```bash
       venv\Scripts\activate
       ```
     - En macOS y Linux:
       ```bash
       source venv/bin/activate
       ```
   - **Instalar las dependencias del proyecto**:
     ```bash
     pip install -r requirements.txt
     ```

3. **Ejecutar los Scripts**:
   - Navega a la carpeta del script que deseas ejecutar. Por ejemplo, para ejecutar el script en `mx_zip_colony`:
     ```bash
     cd mx_zip_colony
     python main.py
     ```
   - Asegúrate de tener los archivos de hoja de cálculo necesarios en la ubicación correcta según lo especificado en cada script.

## Notas Adicionales

- Cada carpeta de script contiene un archivo `README.md` que proporciona información específica sobre el script y su uso.
- Se recomienda revisar la documentación de cada script para entender su funcionalidad y los parámetros que puede aceptar.

## Contribuciones

Si deseas contribuir a este proyecto, no dudes en abrir un issue o enviar un pull request. ¡Agradecemos cualquier mejora o sugerencia!

