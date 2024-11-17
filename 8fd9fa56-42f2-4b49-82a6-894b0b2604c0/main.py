from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import SMA, Slope
from surmount.logging import log

class TradingStrategy(Strategy):

    def __init__(self):
        self.tickers = ["AAPL", "WMT"]

    @property
    def interval(self):
        return "1day"

    @property
    def assets(self):
        return self.tickers

    @property
    def data(self):
        return []

    def run(self, data):
        allocation_dict = {"AAPL": 0, "WMT": 0}  # Initial allocation

        # For each ticker, calculate MA20, MA60, MA240, Slope MA20, and Slope MA60
        for ticker in self.tickers:
            sma20 = SMA(ticker, data["ohlcv"], 20)[-1] if len(SMA(ticker, data["ohlcv"], 20))>0 else None
            sma60 = SMA(ticker, data["ohlcv"], 60)[-1] if len(SMA(ticker, data["ohlcv"], 60))>0 else None
            sma240 = SMA(ticker, data["ohlcv"], 240)[-1] if len(SMA(ticker, data["ohlcv"], 240))>0 else None

            slope_ma20 = Slope(ticker, data["ohlcv"], 20)[-1] if len(Slope(ticker, data["ohlcv"], 20))>0 else None
            slope_ma60 = Slope(ticker, data["ohlcv"], 60)[-1] if len(Slope(ticker, data["ohlcv"], 60))>0 else None
            
            # Decision logic for entering or exiting based on the slope comparison
            if slope_ma20 is not None and slope_ma60 is not None:
                if slope_ma20 > slope_ma60:
                    # Enter condition satisfied, allocate 50%
                    allocation_dict[ticker] = 0.5
                elif slope_ma20 < slope_ma60:
                    # Exit condition satisfied, deallocate
                    allocation_dict[ticker] = 0

        return TargetAllocation(allocation_dict)