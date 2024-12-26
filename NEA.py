import sys
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtCharts import *
from PySide6.QtGui import *
from datetime import datetime

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

        #Configuring axis ranges
        self.startDate = int(datetime.strptime("2024-01-01", "%Y-%m-%d").timestamp())
        self.endDate = int(datetime.strptime("2024-01-10", "%Y-%m-%d").timestamp())

        #Configuring x axis
        self.xAxis = QDateTimeAxis()
        self.xAxis.setTitleText("Day")
        self.xAxis.setFormat("dd-MM-yyyy")
        self.xAxis.setRange(QDateTime.fromSecsSinceEpoch(self.startDate - 86400), QDateTime.fromSecsSinceEpoch(self.endDate))
        self.xAxis.setTickCount((self.endDate - self.startDate) // 86400 + 1)

        #Configuring y axis
        self.yAxis = QValueAxis()
        self.yAxis.setTitleText("Price")
        self.yAxis.setRange(135,150)

        #Adding axes to chart
        self.chart.addAxis(self.xAxis, Qt.AlignBottom)
        self.chart.addAxis(self.yAxis, Qt.AlignLeft)

        self.candlestickChart.attachAxis(self.xAxis)
        self.candlestickChart.attachAxis(self.yAxis)

        #Example data
        data = [
        (datetime(2024, 1, 1).timestamp(), 140, 145, 135, 142),
        (datetime(2024, 1, 2).timestamp(), 141, 144, 138, 140),
        (datetime(2024, 1, 3).timestamp(), 139, 143, 136, 141),
        (datetime(2024, 1, 4).timestamp(), 141, 150, 136, 145),
        ]

        for timestamp, open_, high, low, close in data:
            candlestick = QCandlestickSet(open_, high, low, close, QDateTime.fromSecsSinceEpoch(int(timestamp)).toMSecsSinceEpoch())
            self.candlestickChart.append(candlestick)

        #View chart
        self.chartView = QChartView(self.chart)
        self.chartView.setRenderHint(QPainter.Antialiasing)

        #Configure layout
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