import os
import sys
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFileDialog, QListWidget, QListWidgetItem, QWidget
from PyQt5.QtGui import QPixmap, QCursor
from PyQt5.QtCore import Qt
from PyQt5 import QtCore


class ImageViewer(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setStyleSheet("background-color:#161219;")
        self.setWindowTitle('Image Viewer')
        self.setGeometry(100, 100, 800, 600)

        main_layout = QHBoxLayout()

        # Left side with file list and "Open Image Folder" button
        left_widget = QWidget()
        left_layout = QVBoxLayout()
        left_widget.setLayout(left_layout)
        left_widget.setCursor(QCursor(QtCore.Qt.PointingHandCursor))

        self.file_list_widget = QListWidget(self)
        self.file_list_widget.itemClicked.connect(self.display_image)
        # Set text color and background color for the file list widget items
        self.file_list_widget.setStyleSheet(
            "QListWidget { background-color: purple; }"
            "QListWidget:item { color: white;  }"
        )
        left_layout.addWidget(self.file_list_widget)

        open_button = QPushButton('Open Image Folder', self)
        open_button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        open_button.clicked.connect(self.open_image_folder)
        open_button.setStyleSheet(
            "*{border: 2px solid '#BC006C';" +
            " border-radius: 10px;" +
            " font-size: 20px;" +
            " color: white;" +
            " padding: 10px 0;" +
            " margin:10px 10px ;}" +
            "*:hover{background: '#BC006C';}"
        )
        open_button.setFixedSize(290, 80)
        left_layout.addWidget(open_button)

        # Right side with displayed image
        right_widget = QWidget()
        right_layout = QVBoxLayout()
        right_widget.setLayout(right_layout)

        # Add the "logo6.png" initially visible
        self.logo_label = QLabel()
        logo_pixmap = QPixmap("logo6.png")
        self.logo_label.setPixmap(logo_pixmap)
        self.logo_label.setAlignment(Qt.AlignCenter)
        right_layout.addWidget(self.logo_label)

        self.image_label = QLabel(self)
        right_layout.addWidget(self.image_label)

        main_layout.addWidget(left_widget, 3)  # Adjust proportions as needed
        main_layout.addWidget(right_widget, 7)  # Adjust proportions as needed

        self.setLayout(main_layout)

        self.current_folder = ""

    def open_image_folder(self):
        self.logo_label.hide()  # Hide the logo when the folder is opened
        options = QFileDialog.Options()
        folder_path = QFileDialog.getExistingDirectory(
            self, 'Open Image Folder', options=options)
        if folder_path:
            self.current_folder = folder_path
            self.update_file_list(folder_path)

    def update_file_list(self, folder_path):
        self.file_list_widget.clear()
        for filename in os.listdir(folder_path):
            if filename.lower().endswith((".png", ".gif", ".jpg", ".jpeg", ".bmp")):
                item = QListWidgetItem(filename)
                self.file_list_widget.addItem(item)

    def display_image(self, item):
        if self.current_folder:
            image_path = os.path.join(self.current_folder, item.text())
            pixmap = QPixmap(image_path)
            self.image_label.setPixmap(pixmap)
            self.image_label.adjustSize()


def main():
    app = QApplication(sys.argv)
    viewer = ImageViewer()
    viewer.exec_()  # Use exec_() to show the QDialog as a modal dialog
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
