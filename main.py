import sys
import base64
import os
import time
os.system("title PDF to Base64 Text File")

import random
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QVBoxLayout, QPushButton, QTextEdit, QAction, QMessageBox, QProgressBar, QStyleFactory
from PyQt5.QtCore import Qt, QUrl, QThread, pyqtSignal, QObject
from PyQt5.QtGui import QIcon, QPixmap, QImage
# from PyQt5.QtCore import QDesktopServices

from threading import Thread

# Import base64 encoded icon
from myvar import strIconPNG

from ctypes import windll
windll.shcore.SetProcessDpiAwareness(1)

colors_light = [
    "#7DC343", "#EC722E", "#64A2D8", "#EED842"
]
random_color = random.choice(colors_light)

def decode_base64_to_pdf(base64_data, output_path):
    binary_data = base64.b64decode(base64_data)
    with open(output_path, 'wb') as pdf_file:
        pdf_file.write(binary_data)

class StreamHandler(QObject):
    newText = pyqtSignal(str)

    def write(self, message):
        self.newText.emit(str(message))

    def flush(self):
        pass

class QTextEditHandler:
    def __init__(self, text_edit):
        self.text_edit = text_edit

    def write(self, message):
        self.text_edit.moveCursor(self.text_edit.textCursor().End)
        self.text_edit.insertPlainText(message)
        self.text_edit.ensureCursorVisible()

    def flush(self):
        pass  # This can be left empty

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PDF to Base64 Text File")
        self.setGeometry(100, 100, 400, 600)  # Set window size

        # Set window icon (optional)
        # Set application icon from base64 data
        icon_data = base64.b64decode(strIconPNG())
        image = QImage.fromData(icon_data)
        pixmap = QPixmap.fromImage(image)
        self.setWindowIcon(QIcon(pixmap))

        # Central widget setup
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.central_layout = QVBoxLayout()
        self.central_layout.setContentsMargins(20, 20, 20, 20)
        self.central_widget.setLayout(self.central_layout)

        # Title label
        self.title_label = QLabel("PDF to Base64 Text File")
        self.title_label.setStyleSheet(f"font-size: 28px; font-weight: bold; color: #000000; background-color: {random_color}; padding: 10px;")
        self.central_layout.addWidget(self.title_label, alignment=Qt.AlignCenter)

        # Instruction label
        self.instruction_label = QLabel("Drop files into this window to process them.")
        self.instruction_label.setAlignment(Qt.AlignCenter)
        self.instruction_label.setContentsMargins(0, 20, 0, 0)
        self.central_layout.addWidget(self.instruction_label, alignment=Qt.AlignCenter)

        # Label for dropped file paths (for demonstration)
        self.file_paths_label = QLabel("Dropped files will appear here.")
        self.file_paths_label.setAlignment(Qt.AlignCenter)
        self.file_paths_label.setStyleSheet("text-align: justify;")
        self.file_paths_label.setContentsMargins(0, 0, 0, 20)
        self.central_layout.addWidget(self.file_paths_label)

        # Add a button
        self.process_button = QPushButton("Process Files")
        self.process_button.clicked.connect(self.process_files)
        self.central_layout.addWidget(self.process_button, alignment=Qt.AlignCenter)
        
        self.prg = QProgressBar()
        self.prg.setStyle(QStyleFactory.create("Windows"))
        self.prg.setVisible(False)
        self.prg.setAlignment(Qt.AlignCenter)  # Align text to center
        self.prg.setFormat('%p%')  # Show percentage text
        self.central_layout.addWidget(self.prg)
        
        # Add a button
        self.open_button1 = QPushButton("Open Result File")
        self.open_button1.clicked.connect(self.open_result_file)
        self.central_layout.addWidget(self.open_button1, alignment=Qt.AlignCenter)
        
        # Add a button
        self.open_button = QPushButton("Open Result Folder")
        self.open_button.clicked.connect(self.open_result_folder)
        self.central_layout.addWidget(self.open_button, alignment=Qt.AlignCenter)
        
        # Instruction label
        self.label2 = QLabel("Result files will appear here.")
        self.label2.setAlignment(Qt.AlignCenter)
        self.label2.setContentsMargins(0, 20, 0, 0)
        self.central_layout.addWidget(self.label2, alignment=Qt.AlignCenter)
        
        # Add QTextEdit widget which already has built-in scrolling
        self.text_edit = QTextEdit()
        self.central_layout.addWidget(self.text_edit)

        # Redirect stdout and stderr
        self.stream_handler = StreamHandler()
        self.stream_handler.newText.connect(self.on_new_text)
        sys.stdout = self.stream_handler
        sys.stderr = self.stream_handler

        # Enable drag and drop functionality
        self.setAcceptDrops(True)
        
        # Global variable
        self.dropped_files = []
        self.result_files = []
        
        # self.center_on_screen()
    
    def on_new_text(self, text):
        self.text_edit.moveCursor(self.text_edit.textCursor().End)
        self.text_edit.insertPlainText(text)
        self.text_edit.ensureCursorVisible()
        
    def center_on_screen(self):
        # Function to center the window on the screen
        frame_geometry = self.frameGeometry()
        screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        center_point = QApplication.desktop().screenGeometry(screen).center()
        frame_geometry.moveCenter(center_point)
        self.move(frame_geometry.topLeft())
    
    def worker_finished(self):
        QMessageBox.information(self, "Operation Complete", "The operation has finished successfully.")

    def process_files(self):
        self.worker = WorkerThread(self.dropped_files)
        self.worker.start()
        # self.worker.finished.connect(self.worker_finished)
        self.worker.update_result_files.connect(self.result_files_update)
        self.worker.update_file_paths_label.connect(self.file_paths_label_update)
        
        self.worker.update_prg.connect(self.prg_update)
        self.worker.update_prg_maximum.connect(self.prg_update_maximum)
        self.worker.update_prg_minimum.connect(self.prg_update_minimum)
        self.worker.update_prg_value.connect(self.prg_update_value)
        
        self.worker.update_process_button.connect(self.process_button_update)
        self.worker.update_open_button1.connect(self.open_button1_update)
        self.worker.update_open_button.connect(self.open_button_update)
    
    def process_button_update(self, setEnabled: bool):
        self.process_button.setEnabled(setEnabled)
    
    def open_button1_update(self, setEnabled: bool):
        self.open_button1.setEnabled(setEnabled)
    
    def open_button_update(self, setEnabled: bool):
        self.open_button.setEnabled(setEnabled)
    
    def result_files_update(self, x):
        self.result_files = x
    
    def file_paths_label_update(self, x):
        self.label2 = x
    
    def prg_update(self, x):
        # print(x)
        self.prg.setVisible(x)
        
    # start progress bar
    
    def prg_update_maximum(self, x):
        self.prg.setMaximum(x)
    
    def prg_update_minimum(self, x):
        self.prg.setMinimum(x)
    
    def prg_update_value(self, x):
        self.prg.setValue(x)
    
    # end progress bar
    
    def open_result_file(self):
        if self.result_files:
            first_file = self.result_files[0]
            print(f"Opening result file: {first_file}")
            os.startfile(first_file)
        else:
            print("There's no result yet")
            self.file_paths_label.setText("Drop the file(s) first!")
    
    def open_result_folder(self):
        if self.result_files:
            first_file = self.result_files[0]
            folder_path = os.path.dirname(first_file)
            print(f"Opening result folder: {folder_path}")
            os.startfile(folder_path)
        else:
            print("There's no result yet")
            self.file_paths_label.setText("Drop the file(s) first!")

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        self.dropped_files = [url.toLocalFile() for url in event.mimeData().urls()]
        self.file_paths_label.setText("\n".join(self.dropped_files))

class WorkerThread(QThread):
    update_result_files = pyqtSignal(list)
    update_file_paths_label = pyqtSignal(str)
    update_prg = pyqtSignal(bool)
    update_prg_maximum = pyqtSignal(int)
    update_prg_minimum = pyqtSignal(int)
    update_prg_value = pyqtSignal(int)
    
    update_process_button = pyqtSignal(bool)
    update_open_button1 = pyqtSignal(bool)
    update_open_button = pyqtSignal(bool)
    
    def __init__(self, dropped_files):
        super().__init__()
        self.dropped_files = dropped_files
    
    def pdf_to_blob(self, file_paths):
        
        self.update_prg_maximum.emit(0)
        self.update_prg_maximum.emit(len(file_paths))
        
        progress_value = 0
        self.update_prg_value.emit(progress_value)
        
        output_file_paths = []
        file_count = 1
        for file_path in file_paths:
            try:
                if file_path.lower().endswith('.txt'):
                    # Read the text file containing base64 data
                    with open(file_path, 'r') as txt_file:
                        base64_data = txt_file.read()
                    
                    binary_data = base64.b64decode(base64_data)
                    
                    file_name = os.path.basename(file_path)
                    output_file_name = f'base64_{file_name}.pdf'
                    output_file_path = os.path.join(os.path.dirname(file_path), output_file_name)
                    
                    with open(output_file_path, 'wb') as pdf_file:
                        pdf_file.write(binary_data)
                    
                    output_file_paths.append(output_file_path)
                    
                    print(f"\n=== Output File {file_count}\n{output_file_path}\n")
                    file_count += 1

                else:
                    # Read the PDF file in binary mode
                    with open(file_path, 'rb') as pdf_file:
                        binary_data = pdf_file.read()
                    
                    # Encode the binary data to base64
                    blob_data = base64.b64encode(binary_data).decode('utf-8')
                    
                    # Save base64 data to a text file in the same folder
                    file_name = os.path.basename(file_path)
                    output_file_name = f'base64_{file_name}.txt'
                    output_file_path = os.path.join(os.path.dirname(file_path), output_file_name)
                    
                    with open(output_file_path, 'w') as txt_file:
                        txt_file.write(blob_data)
                    
                    output_file_paths.append(output_file_path)
                    # print(f"Converted {file_path} to base64 and saved to {output_file_path}")
                    
                    print(f"\n=== Output File {file_count}\n{output_file_path}\n")
                    file_count += 1
                
                # end if else
            
            except Exception as e:
                print(f"Error converting {file_path}: {str(e)}")
            
            progress_value += 1
            self.update_prg_value.emit(progress_value)
            # time.sleep(1)
        
        return output_file_paths
    
    def run(self):
        self.update_process_button.emit(False)
        self.update_open_button1.emit(False)
        self.update_open_button.emit(False)
        
        if self.dropped_files:
            self.update_prg.emit(True)
            # for x in range(1, 10):
            #     time.sleep(1)
            #     print(x)
            print("Processing files...")
            self.update_result_files.emit(self.pdf_to_blob(self.dropped_files))
            # self.result_files = pdf_to_blob(self.dropped_files)
            self.update_prg.emit(False)
        else:
            print("There's no file to process")
            self.update_file_paths_label.emit("Drop the file(s) first!")
        
        self.update_process_button.emit(True)
        self.update_open_button1.emit(True)
        self.update_open_button.emit(True)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
