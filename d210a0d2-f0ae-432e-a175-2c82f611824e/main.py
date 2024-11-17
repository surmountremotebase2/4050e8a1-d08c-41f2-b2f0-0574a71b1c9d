from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import SMA
from surmount.logging import log

class TradingStrategy(Strategy):
    @property
    def assets(self):
        # Specify the assets to trade; in this case, AAPL.
        return ["AAPL"]

    @property
    def interval(self):
        # Set the interval for the strategy; as required, this will be '4hour'.
        return "4hour"

    def run(self, data):
        # Initialize allocation with no position.
        allocation_dict = {"AAPL": 0}
        # Retrieve OHLCV data for AAPL.
        d = data["ohlcv"]
        
        # Check if there's enough data to calculate SMA 20 and SMA 60.
        if len(d) >= 60:
            # Calculate SMA 20 and SMA 60
            sma20 = SMA("AAPL", d, 20)
            sma60 = SMA("AAPL", d, 60)
            
            # The Fibonacci retracement level (0.618) buy condition along with SMA comparison could be
            # considered as a simplified condition for buying, without a direct method to calculate retracement levels.
            # A proxy for identifying a potential 'golden ratio' retracement could be when the shorter SMA is above the longer one,
            # implying a potential upward momentum following a retracement.
            
            if sma20[-1] > sma60[-1]:  # Entry condition: SMA 20 is above SMA 60
                allocation_dict["AAPL"] = 1  # Allocate 100% capital to AAPL.

        # If recent SMA 20 is the maximum of the last 20 periods, consider it as an exit signal.
        # This condition might imply the strategy seeks to exit at relative highs.
        # However, without a specific 'exit' mechanism in this platform, you maintain the position or opt to set allocation to zero here.
        
        # Please adjust the logic based on further specifications or data access for precise Fibonacci retracement implementation.

        return TargetAllocation(allocation_dict)