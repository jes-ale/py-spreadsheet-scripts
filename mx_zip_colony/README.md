# Readme mx_zip_colony/correos_de_mexico

## Description
This project aims to process city and postal code (zip code) data files to generate two ODS files with the processed information. 
The city file is exported from Odoo 16+, while the zip code and colony file is obtained from the Correos de México website. The validation file is obtained from the SAT website.
The output consists of two files containing zip codes and colonies, both grouped by city (municipality), ready to be imported into Odoo with the necessary relationships.

Regarding distribution, I am exclusively disseminating the Python script, adhering to the distribution limitations set by Correos de México concerning the sharing of catalogs and processed data.

It's important to note that this script does not automatically add new entries for cities (municipalities) found in the Correos de Mexico catalog.
It retains those record cells as empty (at least it should... maybe it crashes idk you tell me). To address this, it's recommended to either develop a script that identifies and incorporates these new cities or manually create an ODS file for import, the later is especially recommended if the number of newly discovered cities is manageable.

## Usage
1. Download the city and postal code with colony data files from the aforementioned sources.
   - **City File (exported from Odoo 16+)**:
      - Go to contacts > Settings > Cities.
      - Filter by country: México.
      - Modify items per page to show all matches (tested in odoo 17 it had 2458 cities by default, btw i manually added 2 cities to my home state so my use case is for 2460 cities)
      - Select all. Go to actions > export. This will prompt the export wizard for all the selected cities.
      - Check the box to make the exported data compatible with import.
      - Select xlsx format.
      - Remove all the fields for export and add the following: name, l10n_mx_code, external_id, state_name, state_external_id, country_name, country_external_id.
      - Export.
   - **Postal Code and Colony File (obtained from Correos de México)**:
      - Download desired catalogs from [Correos de México](https://www.correosdemexico.gob.mx/SSLServicios/ConsultaCP/CodigoPostal_Exportar.aspx) in Excel format.
      - Remove the first page with the distribution notice.
      - Make sure that the sheet names accurately match the state_name exported from odoo, meaning no underscores, no extra spaces, tildes and so on.
   - **Postal Code and Colony File (obtained from  the SAT)**:
      - Download the catalog for carta porte from [SAT](http://omawww.sat.gob.mx/tramitesyservicios/Paginas/complemento_carta_porte.htm) in Excel format.
      - Remove all sheets but the ones named: c_Colonia_1, c_Colonia_2, and c_Colonia_3.
      - Each sheet should have headers placed on the first row, indicating the respective data fields.
      - The dataset's actual data should commence from row 2, column A, ensuring consistent alignment with the specified headers.
2. Ensure that the files have the correct format and contain the necessary information as described below:
   - **City File (exported from Odoo 16+)**:
     - Required columns: `code`, `name`, `state_code`, `state_name`, `state_external_id`, `country_external_id`.
     - Required name (may be customized on the script entry point): res_city.ods
   - **Postal Code and Colony File (obtained from Correos de México)**:
     - Required columns: `d_asenta`, `id_asenta_cpcons`, `c_mnpio`, `d_codigo`.
     - Required name (may be customized on the script entry point): correos_de_mexico.ods
   - **Postal Code and Colony File (obtained from  the SAT)**:
     - Required columns: `c_Colonia`, `c_CodigoPostal`, `asentamiento`

3. Convert your Excel files to ODS format using the "save as" option in your preferred spreadsheet software. Ensure that the file names match those expected by the script.
3. Place the files in the current project sub-directory.
4. Run the `main.py` script to process the files and generate the output file:
   ```bash
   python main.py
   ```
5. The output file will be available in the same project directory with the specified name in the script.

## Expected Data Format
- **City File**:
  - No output.
- **Postal Code and Colony File**:
  - zip.ods file and colony.ods file.
  - Postal codes and colonies can be in any order.
  - Each row should contain information for one colony with the columns specified above, columns are renamed following this structure:
      'colonies': {
          'name': 'd_asenta',
          'code': 'id_asenta_cpcons',
          'state_name': 'd_estado',
          'city_code': 'c_mnpio',
          'zip': 'd_codigo'
      },
      'zipcodes': {
          'name': 'd_codigo',
          'state_name': 'd_estado',
          'city_code': 'c_mnpio',
      },

## Contributing
If you find any bugs or have ideas to improve the project, you are welcome to contribute! Simply follow these steps:
1. Fork the project.
2. Create a branch for your new feature: `git checkout -b feature/new-feature`.
3. Make your changes and save the files.
4. Commit your changes: `git commit -m 'Add new feature'`.
5. Push your changes to your repository: `git push origin feature/new-feature`.
6. Create a pull request in the original repository.

## License
The goal of this project is to update the database of your Odoo instances. It is not intended for direct commercial use and requires you to be a customer of Correos de México.
The Python script itself is distributed under the MIT License.
