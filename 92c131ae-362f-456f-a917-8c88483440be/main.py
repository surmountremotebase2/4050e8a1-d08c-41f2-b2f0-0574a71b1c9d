from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import SMA, Slope
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        self.tickers = ["AAPL"]

    @property
    def interval(self):
        # Defines the data interval required for indicators calculation
        return "1day"

    @property
    def assets(self):
        # Lists the assets this strategy will cover
        return self.tickers

    def run(self, data):
        allocation_dict = {}
        apple_data = data["ohlcv"]
        
        # Calculate moving averages
        ma20 = SMA("AAPL", apple_data, 20)
        ma60 = SMA("AAPL", apple_data, 60)
        ma240 = SMA("AAPL", apple_data, 240)
        
        # Calculate slopes of the MAs
        slope_ma20 = Slope("AAPL", apple_data, 20)
        slope_ma60 = Slope("AAPL", apple_data, 60)

        # Just a check to make sure we have enough data points for our calculation
        if len(slope_ma20) > 0 and len(slope_ma60) > 0:
            # Decision making based on the slopes of MA20 and MA60
            if slope_ma20[-1] > slope_ma60[-1]:
                # If Slope of MA20 is greater than Slope of MA60, set allocation to AAPL to 1 (enter)
                allocation_dict["AAPL"] = 1
            elif slope_ma20[-1] < slope_ma60[-1]:
                # If Slope of MA20 is less than Slope of MA60, set allocation to AAPL to 0 (exit)
                allocation_dict["AAPL"] = 0
            else:
                # Hold the current position if neither condition is met or no clear signal
                allocation_dict["AAPL"] = 0.5  # or maintain current allocation without change
        else:
            # Log an error or handle the case where we don't have enough data
            log("Not enough data to compute slopes for MA20 and MA60.")

        return TargetAllocation(allocation_dict)