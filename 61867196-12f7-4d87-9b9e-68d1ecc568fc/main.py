from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import SMA, Slope
from surmount.logging import log

class TradingStrategy(Strategy):
    @property
    def assets(self):
        return ["AAPL"]

    @property
    def interval(self):
        return "1day"

    def run(self, data):
        # Initialize allocation to 0
        allocation_dict = {"AAPL": 0}

        # Calculating Moving Averages and their slopes
        ma20 = SMA("AAPL", data["ohlcv"], 20)
        ma60 = SMA("AAPL", data["ohlcv"], 60)
        ma240 = SMA("AAPL", data["ohlcv"], 240)
        slope_ma20 = Slope("AAPL", data["ohlcv"], 20)
        slope_ma60 = Slope("AAPL", data["ohlcv"], 60)

        if len(ma20) > 0 and len(ma60) > 0 and len(slope_ma20) > 0 and len(slope_ma60) > 0:
            # Check if MA20 is greater than MA60, and Slope MA20 is greater than Slope MA60
            if ma20[-1] > ma60[-1] and slope_ma20[-1] > slope_ma60[-1]:
                log("Bullish signal detected, allocating 100% to AAPL")
                allocation_dict["AAPL"] = 1  # Enter position
            else:
                log("Conditions not met for bullish signal, staying out")

            # Exit strategy: If the current value of MA20 is the maximum value in the last 20 periods, exit the position
            if ma20[-1] == max(ma20[-20:]):
                log("MA20 at maximum in last 20 periods, exiting position")
                allocation_dict["AAPL"] = 0  # Exit position

        return TargetAllocation(allocation_dict)