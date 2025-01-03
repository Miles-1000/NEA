import sys
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtCharts import *
from PySide6.QtGui import *
from datetime import datetime, timedelta
from trading_ig import IGService
from trading_ig.config import config

class Display(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupMainGUI()
        self.setupCandlestickChart()

        
    def setupMainGUI(self):
        self.setWindowTitle("Stock Market Trading Algorithm")

        # Setting central widget for QMainWindow 
        centralWidget = QWidget()
        self.setCentralWidget(centralWidget)
        self.mainLayout = QVBoxLayout()

        # Defining dropdown box
        self.algoSelection = QComboBox()
        self.algoSelection.addItems(["No algorithm", "RSI", "Moving average"])

        self.algoSelection.currentIndexChanged.connect(self.changeAlgo)
        
        # Defining text for algorithm selection
        algoSelectText = QLabel("Select algorithm: ")

        # Set layout for top controls
        controlsLayout = QHBoxLayout()
        controlsLayout.addWidget(algoSelectText)
        controlsLayout.addWidget(self.algoSelection)

        # Adding control layout to main
        self.mainLayout.addLayout(controlsLayout)
        centralWidget.setLayout(self.mainLayout)
    
    def setupCandlestickChart(self):
        # Initialise chart
        self.chart = QChart()
        self.chart.setTitle("S&P 500 Chart")

        self.candlestickChart = QCandlestickSeries()
        self.candlestickChart.setName("Stock Candlesticks")
        self.candlestickChart.setIncreasingColor(Qt.green)
        self.candlestickChart.setDecreasingColor(Qt.red)

        self.chart.addSeries(self.candlestickChart)

        # Configuring date ranges
        self.startDate = datetime.strptime("2024-01-10 14:30:00", "%Y-%m-%d %H:%M:%S")
        self.startDateTimestamp = int(self.startDate.timestamp())
        self.endDate = datetime.strptime("2024-01-10 19:00:00", "%Y-%m-%d %H:%M:%S")
        self.endDateTimestamp = int(self.endDate.timestamp())

        # Retrieve data using IG API        
        priceData = self.loadIGData("IX.D.SPTRD.DAILY.IP", "30Min", self.startDate, self.endDate)

        dfAsk = priceData['prices']['ask']

        minPrice = float('inf')
        maxPrice = float('-inf')

        # Iterate through database rows
        for time, price in dfAsk.iterrows():
            # Create new candlestick
            candleStick = QCandlestickSet(
                open = price["Open"],
                high = (highPrice := price["High"]),
                low = (lowPrice := price["Low"]),
                close = price["Close"],
                timestamp = QDateTime.fromSecsSinceEpoch(int(datetime.strptime(str(time), "%Y-%m-%d %H:%M:%S").timestamp())).toMSecsSinceEpoch()
                )

            self.candlestickChart.append(candleStick)
            
            # Keep track of min & max prices
            minPrice = min(minPrice, lowPrice)
            maxPrice = max(maxPrice, highPrice)

        # Configuring x axis
        self.xAxis = QDateTimeAxis()
        self.xAxis.setTitleText("Time")
        self.xAxis.setFormat("HH:mm")

        # Dynamic x range and tick count
        xBuffer = int(timedelta(minutes = 15).total_seconds())
        self.xAxis.setRange(QDateTime.fromSecsSinceEpoch(newStartTime := (self.startDateTimestamp - xBuffer)), QDateTime.fromSecsSinceEpoch(newEndTime := (self.endDateTimestamp + xBuffer)))
        self.xAxis.setTickCount((newEndTime - newStartTime) // (xBuffer * 2) + 1)

        # Configuring y axis
        self.yAxis = QValueAxis()
        self.yAxis.setTitleText("Price")
        
        # Dynamic y range and tick count
        yBuffer = int((maxPrice - minPrice) * 0.1)
        self.yAxis.setRange(newMinPrice := (minPrice - yBuffer), newMaxPrice := (maxPrice + yBuffer))
        self.yAxis.applyNiceNumbers()
        self.yAxis.setMinorTickCount(1)

        # Adding axes to chart
        self.chart.addAxis(self.xAxis, Qt.AlignBottom)
        self.chart.addAxis(self.yAxis, Qt.AlignLeft)

        self.candlestickChart.attachAxis(self.xAxis)
        self.candlestickChart.attachAxis(self.yAxis)

        # View chart
        self.chartView = QChartView(self.chart)
        self.chartView.setRenderHint(QPainter.Antialiasing)

        # Configure layout
        self.mainLayout.addWidget(self.chartView)

    def loadIGData(self, epic, resolution, startDate, endDate):
        # Configure service
        ig_service = IGService(config.username, config.password, config.api_key, config.acc_type)

        ig_service.create_session()

        # Retrieve data
        return ig_service.fetch_historical_prices_by_epic_and_date_range(epic, resolution, startDate.strftime("%Y-%m-%d %H:%M:%S"), endDate.strftime("%Y-%m-%d %H:%M:%S"))


    @Slot(int)
    def changeAlgo(self, index):
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = Display()
    widget.resize(800, 600)
    widget.show()
    sys.exit(app.exec())