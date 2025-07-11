import sys
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtCharts import *
from PySide6.QtGui import *
from datetime import datetime, timedelta, date
from trading_ig import IGService
from trading_ig.config import config

class Display(QMainWindow):
    def __init__(self):
        super().__init__()
        self.IGCache = {}
        self.setupMainGUI()
        self.setupCandlestickChart()
        
    def setupMainGUI(self):
        self.setWindowTitle("Stock Market Trading Algorithm")

        # Setting central widget for QMainWindow 
        centralWidget = QWidget()
        self.setCentralWidget(centralWidget)
        self.mainLayout = QVBoxLayout()

        # Defining date buttons
        self.prevDateButton = QToolButton()
        self.prevDateButton.setArrowType(Qt.LeftArrow)

        self.nextDateButton = QToolButton()
        self.nextDateButton.setArrowType(Qt.RightArrow)
        
        self.prevDateButton.clicked.connect(lambda: self.changeDate(-1))
        self.nextDateButton.clicked.connect(lambda: self.changeDate(1))

        # Label to show date
        self.dateLabel = QLabel()

        # Center widgets
        self.dateLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Set layout for top controls
        controlsLayout = QHBoxLayout()

        controlsLayout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        controlsLayout.addWidget(self.prevDateButton)
        controlsLayout.addWidget(self.dateLabel)
        controlsLayout.addWidget(self.nextDateButton)
        controlsLayout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

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
        self.fetchDate = date.today()
        self.startDate = datetime.strptime(f"{self.fetchDate.strftime("%Y/%m/%d")} 14:30:00", "%Y/%m/%d %H:%M:%S")
        self.endDate = datetime.strptime(f"{self.fetchDate.strftime("%Y/%m/%d")} 19:00:00", "%Y/%m/%d %H:%M:%S")

        self.startDateTimestamp = int(self.startDate.timestamp())
        self.endDateTimestamp = int(self.endDate.timestamp())

        self.dateLabel.setText(datetime.strftime(self.startDate.date(), "%d/%m/%Y"))

        # Retrieve data using IG API        
        priceData = self.loadIGData("IX.D.SPTRD.DAILY.IP", "30Min", self.startDate, self.endDate)

        if priceData:
            minPrice, maxPrice = self.populateChart(priceData)
        else:
            minPrice, maxPrice = 0, 1

        # Configuring x axis
        self.xAxis = QDateTimeAxis()
        self.xAxis.setTitleText("Time")
        self.xAxis.setFormat("HH:mm")

        # Configuring y axis
        self.yAxis = QValueAxis()
        self.yAxis.setTitleText("Price")                
        self.yAxis.applyNiceNumbers()
        self.yAxis.setMinorTickCount(9)

        self.dynamicAxes(int(minPrice), int(maxPrice))
        
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

        try:
            response = self.IGCache[(epic, resolution, startDate, endDate)]
            print("Could find from cache")
        except:
            try:
                response = ig_service.fetch_historical_prices_by_epic_and_date_range(epic, resolution, startDate.strftime("%Y-%m-%d %H:%M:%S"), endDate.strftime("%Y-%m-%d %H:%M:%S"))
            except Exception as error:
                print(error)
                return False
            else:
                self.IGCache.update({(epic, resolution, startDate, endDate): response})
                print("Response", response)
                return response
        else:
            return response


    def populateChart(self, priceData):
        self.candlestickChart.clear()
        
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

        return minPrice, maxPrice

    def dynamicAxes(self, minPrice, maxPrice):
        # Dynamic x range
        xPadding = int(timedelta(minutes = 30).total_seconds())
        self.xAxis.setRange(QDateTime.fromSecsSinceEpoch(newStartTime := (self.startDateTimestamp - xPadding)), QDateTime.fromSecsSinceEpoch(newEndTime := (self.endDateTimestamp + xPadding)))
        self.xAxis.setTickCount((newEndTime - newStartTime) // (xPadding) + 1)
        
        # Dynamic y range
        yPadding = int((maxPrice - minPrice) * 0.1)
        self.yAxis.setRange(minPrice - yPadding, maxPrice + yPadding)
        self.yAxis.applyNiceNumbers()

    @Slot()
    def changeDate(self, sign):
        self.startDate += timedelta(days=1) * sign
        self.endDate += timedelta(days=1) * sign
        self.startDateTimestamp = int(self.startDate.timestamp())
        self.endDateTimestamp = int(self.endDate.timestamp())

        self.dateLabel.setText(datetime.strftime(self.startDate.date(), "%d/%m/%Y"))

        priceData = self.loadIGData("IX.D.SPTRD.DAILY.IP", "30Min", self.startDate, self.endDate)

        if priceData:
            minPrice, maxPrice = self.populateChart(priceData)
            self.dynamicAxes(minPrice, maxPrice)
        else:
            self.candlestickChart.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = Display()
    widget.resize(800, 600)
    widget.show()
    sys.exit(app.exec())