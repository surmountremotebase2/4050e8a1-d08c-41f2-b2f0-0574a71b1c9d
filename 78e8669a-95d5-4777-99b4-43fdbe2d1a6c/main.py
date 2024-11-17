from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import Slope, LOW, HIGH
from surmount.utils import Min, Max
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        # Specify the ticker and timeframe for the strategy.
        self.ticker = "AAPL"
        self.interval = "5min"
    
    @property
    def assets(self):
        return [self.ticker]

    def run(self, data):
        # Initialize allocation dict.
        allocation_dict = {self.ticker: 0}

        # Ensure we have enough data points.
        if len(data["ohlcv"]) < 20:
            return TargetAllocation(allocation_dict)

        # Current and historical lows and highs
        current_low = data["ohlcv"][-1][self.ticker]["low"]
        current_high = data["ohlcv"][-1][self.ticker]["high"]
        
        past_lows = [data["ohlcv"][i][self.ticker]["low"] for i in range(-20, 0)]
        past_highs = [data["ohlcv"][i][self.ticker]["high"] for i in range(-20, 0)]
        
        # Long Recent Low & High
        long_recent_low = min(past_lows + [current_low])
        long_recent_high = max(past_highs + [current_high]) if current_low < long_recent_low else past_highs[-1]

        # Compute Long Recent Low consistency over the past 10 ticks
        consistent_low = all([data["ohlcv"][i][self.ticker]["low"] == long_recent_low for i in range(-10, 0)])

        # Linear regression slope over the last 60 periods
        close_prices = [data["ohlcv"][i][self.ticker]["close"] for i in range(-60, 0) if i >= -60]
        slope = Slope(self.ticker, close_prices, length=60)

        if consistent_low and slope[-1] > slope[0]:  # Entry condition
            allocation_dict[self.ticker] = 1
        elif slope[-1] < slope[-2]:  # Exit condition, assuming peak is when slope turns negative
            allocation_dict[self.ticker] = 0
        else:
            log("Holding position")

        return TargetAllocation(allocation_dict)