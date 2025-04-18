from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton,
                             QFileDialog, QProgressBar, QLabel, QLineEdit, QFormLayout, QMessageBox)
from PyQt5.QtCore import QThread, pyqtSignal
import logging
import os
import sys
import pandas as pd
import ezodf
from pyexcel_ods3 import save_data


def unified_read_file(file_name):
    """Unified function to read CSV, ODS, and XLSX files into DataFrames"""
    file_path = os.path.join(os.getcwd(), file_name)

    if not os.path.exists(file_path):
        print(f"File '{file_name}' not found")
        return None

    try:
        if file_name.endswith('.csv'):
            return {'Sheet1': pd.read_csv(file_path)}
        elif file_name.endswith(('.ods', '.odt')):
            doc = ezodf.opendoc(file_path)
            data_dict = {}
            for sheet in doc.sheets:
                data = []
                for row in sheet.rows():
                    data.append([cell.value if cell.value is not None else '' for cell in row])
                if data:
                    columns = data[0]
                    data_dict[sheet.name] = pd.DataFrame(data[1:], columns=columns)
            return data_dict
        elif file_name.endswith(('.xlsx', '.xls')):
            return pd.read_excel(file_path, sheet_name=None)
        else:
            print("Unsupported file format")
            return None
    except Exception as e:
        print(f"Error reading file: {e}")
        return None


def clean_column(df, column, operations):
    """Generic column cleaning function"""
    if 'strip_spaces' in operations:
        df[column] = df[column].astype(str).str.strip()
    if 'remove_quotes' in operations:
        df[column] = df[column].str.replace("'", "")
    if 'handle_missing' in operations:
        df[column] = df[column].replace('', pd.NA).fillna('0')
    return df


def process_mapping(input_file, output_file, search_col, taken_col, target_col):
    """Process column mapping between two files"""
    input_df = unified_read_file(input_file)['Sheet1']
    output_df = unified_read_file(output_file)['Sheet1']

    mapping = input_df[[search_col, taken_col]].drop_duplicates().set_index(search_col)[taken_col].to_dict()
    output_df[target_col] = output_df[target_col].map(mapping).fillna(output_df[target_col])

    output_df.to_csv(output_file, index=False)
    print(f"Updated {output_file}")


def split_large_file(file_name, max_rows):
    """Split large files into smaller chunks"""
    data_dict = unified_read_file(file_name)
    base_name = os.path.splitext(file_name)[0]

    for sheet_name, df in data_dict.items():
        chunks = [df[i:i + max_rows] for i in range(0, df.shape[0], max_rows)]
        for i, chunk in enumerate(chunks):
            output_name = f"{base_name}_{sheet_name}_part{i + 1}.ods"
            save_data(output_name, {sheet_name: [chunk.columns.tolist()] + chunk.values.tolist()})
            print(f"Created {output_name}")


def interactive_cleaner(file_name, column, operations):
    """Versión modificada para GUI"""
    data_dict = unified_read_file(file_name)

    if not data_dict:
        raise ValueError("Error al leer el archivo")

    sheet = list(data_dict.keys())[0]
    df = data_dict[sheet]

    if column not in df.columns:
        raise ValueError(f"Columna '{column}' no encontrada")

    cleaned_df = clean_column(df.copy(), column, operations)
    output_name = f"cleaned_{os.path.basename(file_name)}"
    cleaned_df.to_csv(output_name, index=False)
    return output_name


# Configuración de logging
logging.basicConfig(
    filename='data_processing.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


class WorkerThread(QThread):
    progress_updated = pyqtSignal(int)
    task_completed = pyqtSignal(bool, str)

    def __init__(self, task_func, *args, **kwargs):
        super().__init__()
        self.task_func = task_func
        self.args = args
        self.kwargs = kwargs

    def run(self):
        try:
            self.task_func(*self.args, **self.kwargs)
            self.task_completed.emit(True, "Operación completada con éxito")
        except Exception as e:
            logging.error(str(e))
            self.task_completed.emit(False, str(e))


class DataProcessorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.current_file = ""
        self.secondary_file = ""

    def init_ui(self):
        self.setWindowTitle('Data Processing Toolkit')
        self.setGeometry(300, 300, 400, 300)

        # Widgets principales
        self.main_widget = QWidget()
        self.layout = QVBoxLayout()

        # Botones principales
        self.btn_mapping = QPushButton('Mapear columnas entre archivos', self)
        self.btn_clean = QPushButton('Limpiar columna específica', self)
        self.btn_split = QPushButton('Dividir archivo grande', self)

        # Barra de progreso
        self.progress_bar = QProgressBar(self)
        self.progress_bar.hide()

        # Diseño
        self.layout.addWidget(self.btn_mapping)
        self.layout.addWidget(self.btn_clean)
        self.layout.addWidget(self.btn_split)
        self.layout.addWidget(self.progress_bar)

        self.main_widget.setLayout(self.layout)
        self.setCentralWidget(self.main_widget)

        # Conexiones
        self.btn_mapping.clicked.connect(self.show_mapping_dialog)
        self.btn_clean.clicked.connect(self.show_clean_dialog)
        self.btn_split.clicked.connect(self.show_split_dialog)

    def show_file_dialog(self, title):
        file_path, _ = QFileDialog.getOpenFileName(
            self, title, "",
            "Archivos de datos (*.csv *.ods *.xlsx *.xls);;Todos los archivos (*)"
        )
        return file_path

    def show_mapping_dialog(self):
        self.mapping_dialog = QWidget()
        layout = QFormLayout()

        self.source_file = QLineEdit()
        self.target_file = QLineEdit()
        self.search_col = QLineEdit()
        self.taken_col = QLineEdit()
        self.target_col = QLineEdit()

        layout.addRow(QLabel('Archivo fuente:'), self.create_file_row(self.source_file))
        layout.addRow(QLabel('Archivo destino:'), self.create_file_row(self.target_file))
        layout.addRow(QLabel('Col. Búsqueda:'), self.search_col)
        layout.addRow(QLabel('Col. Origen:'), self.taken_col)
        layout.addRow(QLabel('Col. Destino:'), self.target_col)

        btn_execute = QPushButton('Ejecutar')
        btn_execute.clicked.connect(self.execute_mapping)

        layout.addRow(btn_execute)
        self.mapping_dialog.setLayout(layout)
        self.mapping_dialog.show()

    def create_file_row(self, line_edit):
        widget = QWidget()
        layout = QVBoxLayout()
        btn_browse = QPushButton('Examinar')
        btn_browse.clicked.connect(lambda: line_edit.setText(self.show_file_dialog("Seleccionar archivo")))
        layout.addWidget(line_edit)
        layout.addWidget(btn_browse)
        widget.setLayout(layout)
        return widget

    def execute_mapping(self):
        if not all([
            self.source_file.text(),
            self.target_file.text(),
            self.search_col.text(),
            self.taken_col.text(),
            self.target_col.text()
        ]):
            QMessageBox.warning(self, "Error", "Todos los campos son requeridos")
            return

        self.worker = WorkerThread(self._mapping_task)
        self.worker.progress_updated.connect(self.update_progress)
        self.worker.task_completed.connect(self.show_result)
        self.progress_bar.show()
        self.worker.start()

    def _mapping_task(self):
        try:
            process_mapping(
                self.source_file.text(),
                self.target_file.text(),
                self.search_col.text(),
                self.taken_col.text(),
                self.target_col.text()
            )
            self.progress_updated.emit(100)
        except Exception as e:
            logging.error(str(e))
            raise

    def update_progress(self, value):
        self.progress_bar.setValue(value)

    def show_result(self, success, message):
        self.progress_bar.hide()
        QMessageBox.information(self,
                                "Resultado",
                                message if success else f"Error: {message}"
                                )

    # Implementar métodos similares para limpieza y división
    def show_clean_dialog(self):
        self.clean_dialog = QWidget()
        layout = QFormLayout()

        self.clean_file = QLineEdit()
        self.clean_column = QLineEdit()
        self.clean_operations = QLineEdit()

        layout.addRow(QLabel('Archivo a limpiar:'), self.create_file_row(self.clean_file))
        layout.addRow(QLabel('Columna a limpiar:'), self.clean_column)
        layout.addRow(QLabel('Operaciones (separadas por espacio):'), self.clean_operations)

        btn_execute = QPushButton('Ejecutar')
        btn_execute.clicked.connect(self.execute_cleaning)

        layout.addRow(btn_execute)
        self.clean_dialog.setLayout(layout)
        self.clean_dialog.show()

    def execute_cleaning(self):
        params = {
            'file_name': self.clean_file.text(),
            'column': self.clean_column.text(),
            'operations': self.clean_operations.text().split()
        }

        if not all(params.values()):
            QMessageBox.warning(self, "Error", "Todos los campos son requeridos")
            return

        self.worker = WorkerThread(
            interactive_cleaner,
            params['file_name'],
            params['column'],
            params['operations']
        )
        self.worker.task_completed.connect(self.show_result)
        self.worker.start()

    def show_split_dialog(self):
        self.split_dialog = QWidget()
        layout = QFormLayout()

        self.split_file = QLineEdit()
        self.split_rows = QLineEdit()

        layout.addRow(QLabel('Archivo a dividir:'), self.create_file_row(self.split_file))
        layout.addRow(QLabel('Máximo de filas por parte:'), self.split_rows)

        btn_execute = QPushButton('Ejecutar')
        btn_execute.clicked.connect(self.execute_splitting)

        layout.addRow(btn_execute)
        self.split_dialog.setLayout(layout)
        self.split_dialog.show()

    def execute_splitting(self):
        try:
            max_rows = int(self.split_rows.text())
            file_path = self.split_file.text()

            if max_rows <= 0:
                raise ValueError
            if not os.path.exists(file_path):
                raise FileNotFoundError

            self.worker = WorkerThread(split_large_file, file_path, max_rows)
            self.worker.task_completed.connect(self.show_result)
            self.worker.start()

        except ValueError:
            QMessageBox.warning(self, "Error", "El número de filas debe ser un entero positivo")
        except FileNotFoundError:
            QMessageBox.warning(self, "Error", "El archivo seleccionado no existe")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DataProcessorApp()
    window.show()
    sys.exit(app.exec_())
