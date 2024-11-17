from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import SMA, Slope
from surmount.data import Asset
from surmount.logging import log
import numpy as np

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
        # Initialize the allocation with no position
        allocation_dict = {"AAPL": 0.0}

        # Getting the close prices for AAPL
        close_prices = [i["AAPL"]["close"] for i in data["ohlcv"]]

        # Calculating Moving Averages
        ma20 = SMA("AAPL", data["ohlcv"], 20)
        ma60 = SMA("AAPL", data["ohlcv"], 60)
        ma240 = SMA("AAPL", data["ohlcv"], 240)

        # Calculating slopes for MA20 and MA60
        slope_ma20 = Slope("AAPL", [{"AAPL": {"close": val}} for val in ma20], len(ma20))
        slope_ma60 = Slope("AAPL", [{"AAPL": {"close": val}} for val in ma60], len(ma60))

        # Calculating the differences between MA20 and MA60
        diff_ma20_ma60 = np.subtract(ma20, ma60)

        # Get the last 20 days of MA20-MA60 difference
        recent_diffs = diff_ma20_ma60[-20:]

        # Strategy logic for entering or exiting positions
        if len(slope_ma20) > 1 and len(slope_ma60) > 1:
            current_slope_ma20 = slope_ma20[-1]
            current_slope_ma60 = slope_ma60[-1]
            current_diff = diff_ma20_ma60[-1]

            # Conditions to enter
            if (current_slope_ma20 > current_slope_ma60) or (current_diff == min(recent_diffs)):
                allocation_dict["AAPL"] = 1.0  # Enter the position by allocating 100% to AAPL
            # Conditions to exit
            elif (current_slope_ma20 < current_slope_ma60) or (current_diff == max(recent_diffs)):
                allocation_dict["AAPL"] = 0.0  # Exit the position by allocating 0% to AAPL

        return TargetAllocation(allocation_dict)