class EmaSimple(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2020, 1, 1)  # Set Start Date
        self.SetEndDate(2020, 4, 1)      #Set End Date
        self.SetCash(100000)             #Set Strategy Cash
        self.AddEquity("WORK", Resolution.Hour)
        self.stock = self.Identity("WORK")
        # self.spyStock = Identity("SPY")
        self.__slow = self.EMA("WORK", 200, Resolution.Hour)
        self.__fast = self.EMA("WORK", 26, Resolution.Hour)
        self.PlotIndicator("WORK", self.__slow, self.stock, self.__fast)
        self.SetWarmUp(200)

        # from System.Drawing import Color

        # stockPlot = Chart("Trade Plot")
        # stockPlot.AddSeries(Series('Buy', SeriesType.Scatter, 0, Color.Green, ScatterMarkerSymbol.Triangle))
        # stockPlot.AddSeries(Series('Sell', SeriesType.Scatter, 0, Color.Red, ScatterMarkerSymbol.TriangleDown))
        
        from System.Drawing import Color
        stockPlot = Chart("Trade Plot")
        stockPlot.AddSeries(Series('Buy', SeriesType.Scatter, '$', Color.Green, ScatterMarkerSymbol.Circle))
        stockPlot.AddSeries(Series('Sell', SeriesType.Scatter, '$', Color.Red, ScatterMarkerSymbol.Circle))
        stockPlot.AddSeries(Series('Stock', SeriesType.Line, '$', Color.Blue))
        self.AddChart(stockPlot)

        
    def OnData(self, data):
        
        if not self.__slow.IsReady: return
        
        
        self.slowEMA = self.__slow.Current.Value 
        self.closePrice = data["WORK"].Price
      
        self.tolerance = 0.0025
        self.stoploss = 0.03
        self.holdings = self.Portfolio["WORK"].Quantity
        
        self.signalDelta = self.closePrice - self.slowEMA
        self.profitPercentage  = self.Portfolio["WORK"].UnrealizedProfitPercent;
        self.Debug(self.profitPercentage)

        self.Plot("Trade Plot","Stock", self.closePrice )
        if self.holdings <= 0 and self.slowEMA > self.closePrice:
            self.SetHoldings("WORK", 1.0)
            self.Plot("Trade Plot", 'Buy', self.closePrice)
            

        elif self.holdings > 0  and (self.profitPercentage < self.stoploss or self.slowEMA < self.closePrice):
            self.Liquidate("WORK")
            self.Plot("Trade Plot", 'Sell', self.closePrice)
            # self.Plot("WORK", 'Sell', self.closePrice)
            print("test")
            
