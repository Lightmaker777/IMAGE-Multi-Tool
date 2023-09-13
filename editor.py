import sys
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QPushButton, QTextBrowser, QLineEdit, QLabel, QHBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QPixmap, QCursor
from PyQt5 import QtCore


class BackgroundRemovalDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Background Removal Tool")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("background-color:#161219;")

# ****************IMAGE URL INPUT*********************
        self.input_label = QLabel("Input Image URL:")
        self.input_label.setStyleSheet(
            "color: white;" +
            " font-size: 20px;"
        )
        self.image_url_input = QLineEdit()
        self.image_url_input.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.image_url_input.setStyleSheet(
            "*{border: 2px solid '#BC006C';" +
            " border-radius: 10px;" +
            " font-size: 20px;" +
            " color: white;" +
            " padding: 10px 0;" +
            " margin:10px 10px ;}"

        )
        self.image_url_input.setPlaceholderText("Input Image URL")
# *************BACKGROUND IMAGE URL INPUT****************
        self.background_label = QLabel("Input Background Image URL:")
        self.background_label.setStyleSheet(
            "color: white;" +
            " font-size: 20px;"
        )

        self.background_url_input = QLineEdit()
        self.background_url_input.setCursor(
            QCursor(QtCore.Qt.PointingHandCursor))
        self.background_url_input.setStyleSheet(
            "*{border: 2px solid '#BC006C';" +
            " border-radius: 10px;" +
            " font-size: 20px;" +
            " color: white;" +
            " padding: 10px 0;" +
            " margin:10px 10px ;}" +
            "*::placeholder { color: white; }"

        )
        self.background_url_input.setPlaceholderText(
            "Input Background Image URL")
# ****************RUN BUTTON*********************
        self.run_button = QPushButton("Run Background Removal")
        self.run_button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.run_button.setStyleSheet(
            "*{border: 2px solid '#BC006C';" +
            " border-radius: 10px;" +
            "color: white;" +
            " font-size: 20px;" +
            " padding: 10px 0;" +
            " margin:10px 10px ;}" +
            "*:hover{background: '#BC006C';}"

        )

        self.masked_image_label = QLabel()
        layout = QVBoxLayout()
        layout.addWidget(self.image_url_input)
        layout.addWidget(self.background_url_input)
        layout.addWidget(self.run_button)
        layout.addWidget(self.masked_image_label)

        self.setLayout(layout)

        self.run_button.clicked.connect(self.runBackgroundRemoval)

    def runBackgroundRemoval(self):
        # Get the input URLs from the QLineEdit widgets
        image_url = self.image_url_input.text()
        background_url = self.background_url_input.text()

        from rembg import remove
        import requests
        from PIL import Image
        from io import BytesIO
        import os

        # create the directories if they don't exist
        os.makedirs('original', exist_ok=True)
        os.makedirs('masked', exist_ok=True)

        # save the image locally and mask it
        img_name = image_url.split('/')[-1]
        img = Image.open(BytesIO(requests.get(image_url).content))
        img.save('original/' + img_name, format='jpeg')

        output_path = 'masked/' + img_name

        with open(output_path, 'wb') as f:
            input_data = open('original/' + img_name, 'rb').read()
            subject = remove(input_data, alpha_matting=True, alpha_matting_foreground_threshold=240,
                             alpha_matting_background_threshold=10)
            f.write(subject)

        background_img_name = background_url.split('/')[-1]
        background_img = Image.open(
            BytesIO(requests.get(background_url).content))
        background_img = background_img.resize((img.width, img.height))

        foreground_img = Image.open(output_path)
        background_img.paste(foreground_img, (0, 0), foreground_img)
        background_img.save('masked/background.jpg', format='jpeg')

        # Display the masked image
        masked_image_path = 'masked/background.jpg'
        pixmap = QPixmap(masked_image_path)
        self.masked_image_label.setPixmap(pixmap)
        self.masked_image_label.setScaledContents(True)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    dialog = BackgroundRemovalDialog()
    dialog.show()
    sys.exit(app.exec_())
