from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import RSI, EMA, SMA, MACD, MFI, BB
from surmount.logging import log
from surmount.data import Asset

class TradingStrategy(Strategy):
    
    @property
    def assets(self):
        return ["AAPL"]

    @property
    def interval(self):
        return "1hour"
    
    def run(self, data):
        # Retrieve the closing prices for AAPL
        closes = [x["AAPL"]["close"] for x in data["ohlcv"]]
        
        # Simplistic approach to identify a recent high and low for calculating Fibonacci level
        # In a more realistic scenario, you'd want to identify significant highs and lows
        recent_high = max(closes[-24:])  # High of the last 24 hours
        recent_low = min(closes[-24:])   # Low of the last 24 hours
        
        # Calculate the Fibonacci 0.618 level
        fib_0618 = recent_low + (recent_high - recent_low) * 0.618
        
        current_price = closes[-1]
        allocation = 0
        
        # Example strategy: go long (1) if the price is above the 0.618 retracement level
        # implying an expectation of reversal or continuation of the uptrend
        if current_price > fib_0618:
            allocation = 1  # full investment in AAPL
        else:
            allocation = 0  # no investment in AAPL

        # Log the calculated Fibonacci level for monitoring
        log(f"Fibonacci 0.618 level for AAPL: {fib_0618}, Current Price: {current_price}")

        return TargetAllocation({"AAPL": allocation})