# pip install openai dotenv PyQt5 ...
import sys
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget, QDialog, QGridLayout, QMainWindow, QLineEdit, QHBoxLayout
from PyQt5.QtGui import QPixmap, QCursor
from PyQt5 import QtCore
from base64 import b64decode
from PyQt5.QtCore import QSize, Qt
import os
import json
from dotenv import load_dotenv
import openai
# import files
from img_viewer import ImageViewer
from editor import BackgroundRemovalDialog

app = QApplication(sys.argv)


widgets = {
    "logo": [],
    "button": [],
}
# Define frame variables
frame1 = None
frame2 = None
frame3 = None
frame4 = None
frame5 = None

# ***************************WELCOME*****************************************


def create_frame1():
    global frame1
    frame = QWidget()
    frame_layout = QVBoxLayout()
# Display logo for frame 1
    logo1 = QLabel()
    logo1.setPixmap(QPixmap("logo.png"))
    logo1.setAlignment(QtCore.Qt.AlignCenter)
    logo1.setStyleSheet("margin-top: 100px; ")

# Button for frame 1
    button1 = QPushButton("START")
    button1.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    button1.setStyleSheet(
        "*{border: 4px solid '#BC006C';" +
        " border-radius: 45px;" +
        " font-size: 35px;" +
        " color: white;" +
        " padding: 25px 0;" +
        " margin: 100px 200px;}" +
        "*:hover{background: '#BC006C';}"
    )

    frame_layout.addWidget(logo1)
    frame_layout.addWidget(button1)
    frame.setLayout(frame_layout)

    return frame
# **************************MENU BUTTONS***************************


def create_frame2():
    global frame2
    frame = QWidget()
    frame_layout = QVBoxLayout()

    # Display logo for frame 2
    logo2 = QLabel()
    logo2.setPixmap(QPixmap("logo5.png"))
    logo2.setAlignment(QtCore.Qt.AlignCenter)
    logo2.setStyleSheet("margin-top: 100px; ")

    # Buttons for frame 2
    button2 = QPushButton("GENERATOR")
    button3 = QPushButton("IMAGE VIEWER")
    button4 = QPushButton("IMAGE EDITOR")
     

    # Set object names for the buttons
    button2.setObjectName("GENERATOR")
    button3.setObjectName("IMAGE VIEWER")
    button4.setObjectName("IMAGE EDITOR")
   

    buttons = [button2, button3, button4]
    for button in buttons:
        button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        button.setStyleSheet(
            "*{border: 4px solid '#BC006C';" +
            " border-radius: 45px;" +
            " font-size: 35px;" +
            " color: white;" +
            " padding: 25px 0;" +
            " margin: 10px 200px;}" +
            "*:hover{background: '#BC006C';}"
        )

    frame_layout.addWidget(logo2)
    frame_layout.addWidget(button2)
    frame_layout.addWidget(button3)
    frame_layout.addWidget(button4)
    frame.setLayout(frame_layout)

    # Connect the buttons to the corresponding frame switch functions
    button2.clicked.connect(switch_to_frame3)  # GENERATOR button
    button3.clicked.connect(switch_to_frame4)  # IMAGE VIEWER button
    button4.clicked.connect(switch_to_frame5)  # IMAGE EDITOR button

    return frame

# ************************GENERATOR*********************


class ImageViewerDialog(QDialog):
    def __init__(self, image_path):
        super().__init__()

        # Load the image to determine its size
        pixmap = QPixmap(image_path)
        image_width = pixmap.width()
        image_height = pixmap.height()

        # Set the dialog's size to match the image's size
        self.setFixedSize(image_width, image_height)

        self.setWindowTitle("Generated Image")

        # Set black background color
        self.setStyleSheet("background-color: black;")

        layout = QVBoxLayout()
        image_label = QLabel()
        image_label.setPixmap(pixmap)

        # Center the image horizontally and vertically
        center_layout = QHBoxLayout()
        center_layout.addWidget(image_label, alignment=Qt.AlignCenter)
        layout.addLayout(center_layout)

        self.setLayout(layout)

    def load_image(self, image_path):
        pixmap = QPixmap(image_path)
        self.image_label.setPixmap(pixmap)
        self.image_label.setAlignment(Qt.AlignCenter)


def generate_image(api_key, prompt):
    openai.api_key = api_key
    response = openai.Image.create(
        prompt=prompt,
        n=1,
        size="512x512",
        response_format="b64_json"
    )
    save_image_data(response, prompt)
    return response


def save_image_data(response, prompt_text):
    image_data = b64decode(response["data"][0]["b64_json"])
    file_name = "_".join(prompt_text.split(" "))
    file_path = os.path.join("images", f"{file_name}.png")

    with open(file_path, "wb") as file:
        file.write(image_data)
 # ********************************************************************


def create_frame3():
    global frame3
    frame = QWidget()
    frame_layout = QVBoxLayout()

    # Display logo for frame 3
    logo3 = QLabel()
    logo3.setPixmap(QPixmap("logo4.png"))
    logo3.setAlignment(QtCore.Qt.AlignCenter)
    logo3.setStyleSheet("margin-top: 100px; ")

   # Add a text input field
    text_input = QLineEdit()
    text_input.setPlaceholderText("Describe the image you want to generate")
    text_input.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    text_input.setStyleSheet(
        "*{border: 4px solid '#BC006C';" +
        " border-radius: 45px;" +
        " font-size: 35px;" +
        " color: white;" +
        " padding: 25px 0;" +
        " margin: 10px 10px ;}"

    )
    # Add a "Generate Image" button
    generate_button = QPushButton("Generate Image")
    generate_button.setCursor(Qt.PointingHandCursor)
    generate_button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    generate_button.setStyleSheet(
        "*{border: 4px solid '#BC006C';" +
        " border-radius: 45px;" +
        " font-size: 35px;" +
        " color: white;" +
        " padding: 25px 0;" +
        " margin: 10px 200px ;}" +
        "*:hover{background: '#BC006C';}"

    )
    # Add an image label to display the generated image
    image_label = QLabel()

    # Add a "Back" button to return to frame2
    back_button = QPushButton("Back")
    back_button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    back_button.setObjectName("Back")  # Set the object name here
    back_button.setStyleSheet(
        "*{border: 4px solid '#BC006C';" +
        " border-radius: 45px;" +
        " font-size: 35px;" +
        " color: white;" +
        " padding: 25px 0;" +
        " margin: 10px 200px ;}" +
        "*:hover{background: '#BC006C';}"
    )
    back_button.clicked.connect(switch_to_frame2)

   # Connect the button click to generate and display the image
    generate_button.clicked.connect(lambda: generate_and_display_image(
        api_key, text_input.text(), image_label))

    frame_layout.addWidget(logo3)
    frame_layout.addWidget(text_input)
    frame_layout.addWidget(generate_button)
    frame_layout.addWidget(back_button)
    frame_layout.addWidget(image_label)
    frame.setLayout(frame_layout)

    return frame


def generate_and_display_image(api_key, prompt, image_label):
    response = generate_image(api_key, prompt)

    # Save the generated image
    save_image_data(response, prompt)

    # Get the image path
    file_name = "__".join(prompt.split(" "))
    image_path = os.path.join("images", f"{file_name}.png")

    # Show the image viewer dialog
    image_viewer_dialog = ImageViewerDialog(image_path)
    image_viewer_dialog.exec_()


def save_image_data(response, prompt_text):
    image_data = b64decode(response["data"][0]["b64_json"])
    file_name = "__".join(prompt_text.split(" "))
    directory = "images"  # Directory where you want to save images

    # Create the directory if it doesn't exist
    if not os.path.exists(directory):
        os.makedirs(directory)

    file_path = os.path.join(directory, f"{file_name}.png")

    with open(file_path, "wb") as file:
        file.write(image_data)

# ************************IMAGE VIEWER********************************************


def create_frame4():
    global frame4
    frame = QWidget()
    frame_layout = QVBoxLayout()

    # Display logo for frame 4
    logo4 = QLabel()
    logo4.setPixmap(QPixmap("logo2.png"))  # Change the logo path as needed
    logo4.setAlignment(QtCore.Qt.AlignCenter)
    logo4.setStyleSheet("margin-top: 100px; ")

    # Create a button to open the ImageViewer
    open_viewer_button = QPushButton('Open Image Viewer', frame)
    open_viewer_button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))

    # Connect the button to a function that will open the ImageViewer
    open_viewer_button.clicked.connect(open_image_viewer)

    open_viewer_button.setStyleSheet(
        "*{border: 4px solid '#BC006C';" +
        " border-radius: 45px;" +
        " font-size: 35px;" +
        " color: white;" +
        " padding: 25px 0;" +
        " margin: 10px 200px;}" +
        "*:hover{background: '#BC006C';}"
    )

    # Add a "Back" button to return to frame2
    back_button = QPushButton("Back")
    back_button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    back_button.setObjectName("Back")  # Set the object name here
    back_button.setStyleSheet(
        "*{border: 4px solid '#BC006C';" +
        " border-radius: 45px;" +
        " font-size: 35px;" +
        " color: white;" +
        " padding: 25px 0;" +
        " margin: 10px 200px ;}" +
        "*:hover{background: '#BC006C';}"
    )
    back_button.clicked.connect(switch_to_frame2)

    frame_layout.addWidget(logo4)
    frame_layout.addWidget(open_viewer_button)
    frame_layout.addWidget(back_button)
    frame.setLayout(frame_layout)

    return frame


def open_image_viewer():
    # Create an instance of the ImageViewer class (from img_viewer.py)
    image_viewer = ImageViewer()
    # Show the ImageViewer dialog
    result = image_viewer.exec_()

# *********************************EDITOR********************************


def create_frame5():
    global frame5
    frame = QWidget()
    frame_layout = QVBoxLayout()

    # Display logo for frame 5
    logo5 = QLabel()
    logo5.setPixmap(QPixmap("logo3.png"))  # Change the logo path as needed
    logo5.setAlignment(QtCore.Qt.AlignCenter)
    logo5.setStyleSheet("margin-top: 100px; ")

    # Add a "editor" button to perform the operation
    editor_button = QPushButton("OPEN IMAGE EDITOR")
    editor_button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    editor_button.setObjectName("OPEN IMAGE EDITOR")  # Set the object name here
    editor_button.setStyleSheet(
        "*{border: 4px solid '#BC006C';" +
        " border-radius: 45px;" +
        " font-size: 35px;" +
        " color: white;" +
        " padding: 25px 0;" +
        " margin: 10px 200px;}" +
        "*:hover{background: '#BC006C';}"
    )

    # Add a "Back" button to return to frame2
    back_button = QPushButton("Back")
    back_button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    back_button.setObjectName("Back")
    back_button.setStyleSheet(
        "*{border: 4px solid '#BC006C';" +
        " border-radius: 45px;" +
        " font-size: 35px;" +
        " color: white;" +
        " padding: 25px 0;" +
        " margin: 10px 200px ;}" +
        "*:hover{background: '#BC006C';}"
    )
    back_button.clicked.connect(switch_to_frame2)

    # Connect the "editor" button to switch to frame2 after execution
    editor_button.clicked.connect(switch_to_frame2)

    frame_layout.addWidget(logo5)
    frame_layout.addWidget(editor_button)
    frame_layout.addWidget(back_button)
    frame.setLayout(frame_layout)

    return frame


# *************************************************************************************


def switch_to_frame2():
    global frame2  # Ensure frame is accessible globally
    frame2 = create_frame2()
    main_window.setCentralWidget(frame2)


def switch_to_frame3():
    global frame3
    frame3 = create_frame3()
    main_window.setCentralWidget(frame3)


def switch_to_frame4():
    global frame4
    frame4 = create_frame4()
    main_window.setCentralWidget(frame4)


def switch_to_frame5():
    global frame5
    frame5 = create_frame5()
    main_window.setCentralWidget(frame5)
    # Connect the "OPEN IMAGE EDITOR" button to open the editor window
    editor_button = frame5.findChild(QPushButton, "OPEN IMAGE EDITOR")
    editor_button.clicked.connect(open_image_editor)
def open_image_editor():
    # Create an instance of the BackgroundRemovalDialog and show it
    editor_dialog = BackgroundRemovalDialog()
    editor_dialog.exec_()

# Create the main window as a QMainWindow***********************************************
main_window = QMainWindow()
main_window.setWindowTitle("IMAGE Generator-MultiApp")
main_window.setFixedWidth(1000)
main_window.move(2700, 200)
main_window.setStyleSheet("background: #161219;")

# Create frames
frame1 = create_frame1()
frame2 = create_frame2()
frame3 = create_frame3()
frame4 = create_frame4()
frame5 = create_frame5()

# Set frame1 as the initial central widget
main_window.setCentralWidget(frame1)

# Connect the buttons in frames to switch to the corresponding frames
frame1.layout().itemAt(1).widget().clicked.connect(
    switch_to_frame2)  # START button
frame2.findChild(QPushButton, "GENERATOR").clicked.connect(
    switch_to_frame3)  # GENERATOR button
frame2.findChild(QPushButton, "IMAGE VIEWER").clicked.connect(
    switch_to_frame4)  # IMAGE VIEWER button
frame2.findChild(QPushButton, "IMAGE EDITOR").clicked.connect(
    switch_to_frame5)  # EDITOR button
frame3.findChild(QPushButton, "Back").clicked.connect(
    switch_to_frame2)  # Back button
frame4.findChild(QPushButton, "Back").clicked.connect(
    switch_to_frame2)  # Back button
frame5.findChild(QPushButton, "Back").clicked.connect(
    switch_to_frame2)  # Back button


# Load API key and start the application
if __name__ == "__main__":
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    main_window.show()
    sys.exit(app.exec_())
