from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import SMA, Slope
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        self.tickers = ["AAPL"]

    @property
    def assets(self):
        return self.tickers

    @property
    def interval(self):
        return "1day"

    def run(self, data):
        # Initialize allocation
        allocation_dict = {ticker: 0 for ticker in self.tickers}
        
        # Calculate MAs and slopes
        ma20 = SMA("AAPL", data["ohlcv"], 20)
        ma60 = SMA("AAPL", data["ohlcv"], 60)
        ma240 = SMA("AAPL", data["ohlcv"], 240)
        slope_ma20 = Slope("AAPL", data["ohlcv"], 20)
        slope_ma60 = Slope("AAPL", data["ohlcv"], 60)
        
        # Ensure there is enough data points to proceed
        if len(ma20) > 20 and len(ma60) > 20 and len(slope_ma20) > 0 and len(slope_ma60) > 0:
            difference_ma20_ma60 = [ma20[i] - ma60[i] for i in range(len(ma20))]
            
            # Enter condition (slope MA20 > slope MA60)
            if slope_ma20[-1] > slope_ma60[-1]:
                allocation_dict["AAPL"] = 1.0  # Enter position (100% allocation)
            
            # Exit condition
            if max(difference_ma20_ma60[-20:]) == difference_ma20_ma60[-1]:
                allocation_dict["AAPL"] = 0  # Exit position
            
        log(f"Allocations: {allocation_dict}")
        return TargetAllocation(allocation_dict)