import sys
import base64
import os
os.system("title PDF to Base64 Text File")

import random
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QVBoxLayout, QPushButton, QTextEdit, QAction
from PyQt5.QtCore import Qt, QUrl
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

def pdf_to_blob(file_paths):
    output_file_paths = []
    file_count = 1
    for file_path in file_paths:
        try:
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
        
        except Exception as e:
            print(f"Error converting {file_path}: {str(e)}")
    
    return output_file_paths

class ConsoleWidget(QTextEdit):
    def __init__(self):
        super().__init__()
        self.setReadOnly(True)

    def write(self, text):
        self.moveCursor(self.textCursor().End)
        self.insertPlainText(text)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PDF to Base64 Text File")
        self.setGeometry(100, 100, 600, 800)  # Set window size

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
        self.title_label.setStyleSheet(f"font-size: 28px; font-weight: bold; color: #333333; background-color: {random_color}; padding: 10px;")
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
        
        # Console widget to display output
        self.console_widget = ConsoleWidget()
        self.central_layout.addWidget(self.console_widget)

        # Redirect stdout and stderr
        sys.stdout = self.console_widget
        sys.stderr = self.console_widget

        # Enable drag and drop functionality
        self.setAcceptDrops(True)
        
        # Global variable
        self.dropped_files = []
        self.result_files = []
        
        # self.center_on_screen()
        
    def center_on_screen(self):
        # Function to center the window on the screen
        frame_geometry = self.frameGeometry()
        screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        center_point = QApplication.desktop().screenGeometry(screen).center()
        frame_geometry.moveCenter(center_point)
        self.move(frame_geometry.topLeft())

    def start_process_files(self):
        Thread(target=self.process_files).start()

    def process_files(self):
        # Dummy function to handle processing of files
        # Replace with your actual processing logic
        if self.dropped_files:
            print("Processing files...")
            # print("Files:", dropped_files)
            
            self.result_files = pdf_to_blob(self.dropped_files)
        else:
            print("There's no file to process")
            self.file_paths_label.setText("Drop the file(s) first!")
    
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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
