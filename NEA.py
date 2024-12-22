import sys
#from PySide6 import QtCore, QtWidgets, QtGui, QtGraphs
from PySide6 import QtWidgets, QtCore

class Display(QtWidgets.QWidget):
    def __init__(self, algos):
        super().__init__()

        self.algos = algos
        
        self.setWindowTitle("Stock Market Trading Algorithm")
        self.algoSelection = QtWidgets.QComboBox()
        self.algoSelection.addItems(algos)
        self.choiceDisplay = QtWidgets.QLabel()
        self.choiceDisplay.setText("No algorithm selected yet")
        self.layout = QtWidgets.QVBoxLayout()

        self.layout.addWidget(self.algoSelection)
        self.layout.addWidget(self.choiceDisplay)
        self.setLayout(self.layout)

        self.algoSelection.currentIndexChanged.connect(self.changeAlgo)

    @QtCore.Slot()
    def changeAlgo(self, index):
        self.choiceDisplay.setText("Current Algorithm: " + self.algos[index])


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    widget = Display(["RSI", "Moving average", "Custom"])
    widget.resize(800, 600)
    widget.show()
    sys.exit(app.exec())