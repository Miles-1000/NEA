import sys
#from PySide6 import QtCore, QtWidgets, QtGui, QtGraphs
from PySide6 import QtWidgets, QtCore

class MainGUI(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        
        self.button = QtWidgets.QPushButton("Buttony wuttony")
        self.line_edit = QtWidgets.QLineEdit()
        self.line_edit.setPlaceholderText("Button not pressed yet :(")
        self.text_edit = QtWidgets.QTextEdit()
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.line_edit)
        self.layout.addWidget(self.button)
        self.layout.addWidget(self.text_edit)

        self.button.clicked.connect(self.buttonPress)

    @QtCore.Slot()
    def buttonPress(self):
        self.line_edit.setPlaceholderText("Button pressed!! YAY :DD")
        self.text_edit.append(self.line_edit.text())

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    widget = MainGUI()
    widget.resize(800, 600)
    widget.show()
    sys.exit(app.exec())