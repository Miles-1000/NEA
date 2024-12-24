import sys
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtCharts import *
from PySide6.QtGui import *

class Display(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupMainGUI()
        self.setupCandlestickChart()

        
    def setupMainGUI(self):
        self.setWindowTitle("Stock Market Trading Algorithm")

        #Setting central widget for QMainWindow 
        centralWidget = QWidget()
        self.setCentralWidget(centralWidget)
        self.mainLayout = QVBoxLayout()

        #Defining dropdown box
        self.algoSelection = QComboBox()
        self.algoSelection.addItems(["No algorithm", "RSI", "Moving average"])

        self.algoSelection.currentIndexChanged.connect(self.changeAlgo)
        
        #Defining text for algorithm selection
        algoSelectText = QLabel("Select algorithm: ")

        #Set layout for top controls
        controlsLayout = QHBoxLayout()
        controlsLayout.addWidget(algoSelectText)
        controlsLayout.addWidget(self.algoSelection)

        #Adding control layout to main
        self.mainLayout.addLayout(controlsLayout)
        centralWidget.setLayout(self.mainLayout)
    
    def setupCandlestickChart(self):
        #Initialise chart
        self.chart = QChart()
        self.chart.setTitle("Example Chart")

        self.candlestickChart = QCandlestickSeries()
        self.candlestickChart.setName("Stock Candlesticks")
        self.candlestickChart.setIncreasingColor(Qt.green)
        self.candlestickChart.setDecreasingColor(Qt.red)

        self.chart.addSeries(self.candlestickChart)

        #Configuring axes
        self.xAxis = QValueAxis()
        self.yAxis = QValueAxis()

        self.xAxis.setTitleText("Day")
        self.yAxis.setTitleText("Price")

        self.xAxis.setRange(0,9)
        self.xAxis.setTickCount(15)
        self.yAxis.setRange(135,150)

        self.chart.addAxis(self.xAxis, Qt.AlignBottom)
        self.chart.addAxis(self.yAxis, Qt.AlignLeft)

        self.candlestickChart.attachAxis(self.xAxis)
        self.candlestickChart.attachAxis(self.yAxis)

        self.chartView = QChartView(self.chart)
        self.chartView.setRenderHint(QPainter.Antialiasing)

        self.mainLayout.addWidget(self.chartView)

    @Slot(int)
    def changeAlgo(self, index):
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = Display()
    widget.resize(800, 600)
    widget.show()
    sys.exit(app.exec())