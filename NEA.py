import sys
#from PySide6 import QtCore, QtWidgets, QtGui, QtGraphs
from PySide6 import QtWidgets, QtCore

class MainGUI(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        
        self.button = QtWidgets.QPushButton("Buttony wuttony")
        self.input_box = QtWidgets.QLineEdit()
        self.input_box.setPlaceholderText("Button not pressed yet :(")
        self.text_edit = QtWidgets.QTextEdit()
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.input_box)
        self.layout.addWidget(self.button)
        self.layout.addWidget(self.text_edit)

        self.button.clicked.connect(self.inputEntered)
        self.button.clicked.connect(self.buttonPressed)
        self.input_box.returnPressed.connect(self.inputEntered)

    @QtCore.Slot()
    def inputEntered(self):
        self.text_edit.append(self.input_box.text())
        self.input_box.setText("")

    def buttonPressed(self):
        self.input_box.setPlaceholderText("Button pressed!! YAY :DD")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    widget = MainGUI()
    widget.resize(800, 600)
    widget.show()
    sys.exit(app.exec())