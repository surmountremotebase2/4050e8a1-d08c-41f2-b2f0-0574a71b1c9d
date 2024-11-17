from surmount.base_class import Strategy, TargetAllocation
from surmount.data import Asset
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        self.tickers = ["AAPL"]  # Set the tickers you are interested in

    @property
    def assets(self):
        return self.tickers

    @property
    def interval(self):
        return "4hour"  # Set the interval for data collection

    def run(self, data):
        """
        Main method where trading logic is implemented.
        Calculate Fibonacci Retracement level of 0.618 as a potential support or resistance.
        This example assumes you have predefined the period to calculate high and low.
        In practice, you'd dynamically calculate these over a significant trend.
        """
        
        # Assuming 'high' and 'low' are obtained from previous significant price movement trends
        high = max(i["AAPL"]["high"] for i in data["ohlcv"])  # This should be adjusted to identify the actual high in a real trend
        low = min(i["AAPL"]["low"] for i in data["ohlcv"])  # Similarly, find the actual low in the trend
        
        # Calculate the Fibonacci Retracement level of 0.618
        fib_618 = low + (high - low) * 0.618
        
        # Current price for simplicity; in practice, consider closing prices or live prices
        current_price = data["ohlcv"][-1]["AAPL"]["close"]
        
        log("Fibonacci 0.618 Level: " + str(fib_618))
        
        # Example strategy: buy if current price is just above Fibonacci 0.618 level, signalling potential support
        # This can be adjusted based on tolerance or other indicators for entry
        allocation = 0
        if current_price > fib_618 and current_price < fib_618 * 1.01: # 1% tolerance above the 0.618 level
            allocation = 1  # Allocate 100% to AAPL
            
        # Adjust allocation strategy as needed
        return TargetAllocation({"AAPL": allocation})