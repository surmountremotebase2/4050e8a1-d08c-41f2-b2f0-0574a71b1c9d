from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import SMA, Slope
from surmount.data import Asset

class TradingStrategy(Strategy):
    def __init__(self):
        self.tickers = ["AAPL"]

    @property
    def interval(self):
        return "1day"

    @property
    def assets(self):
        return self.tickers

    def run(self, data):
        # Calculate moving averages
        ma20 = SMA("AAPL", data["ohlcv"], 20)
        ma60 = SMA("AAPL", data["ohlcv"], 60)
        ma240 = SMA("AAPL", data["ohlcv"], 240)

        # Calculate slopes
        slope_ma20 = Slope("AAPL", data["ohlcv"], 20)
        slope_ma60 = Slope("AAPL", data["ohlcv"], 60)

        # Calculate MA20 - MA60
        ma_diff = list(map(lambda x, y: x - y, ma20, ma60))

        # Entry and exit conditions
        # Assuming that 'max' functions return the last value as the "current" date max due to sequential calculation.
        enter_condition = (slope_ma20[-1] == max(slope_ma20)) and \
                          (slope_ma60[-1] == max(slope_ma60)) and \
                          (ma_diff[-1] == max(ma_diff))

        exit_condition = (slope_ma20[-1] != max(slope_ma20)) and \
                         (slope_ma60[-1] != max(slope_ma60)) and \
                         (ma_diff[-1] == max(ma_diff))

        allocation_dict = {}

        if enter_condition:
            allocation_dict["AAPL"] = 1.0  # Enter position
        elif exit_condition:
            allocation_dict["AAPL"] = 0  # Exit position
        else:
            allocation_dict["AAPL"] = 0  # Default to no position if conditions don't match

        return TargetAllocation(allocation_dict)