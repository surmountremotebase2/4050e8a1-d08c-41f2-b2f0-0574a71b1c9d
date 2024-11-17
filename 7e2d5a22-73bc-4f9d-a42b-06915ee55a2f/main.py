from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import SMA, Momentum
from surmount.logging import log
from surmount.data import Asset
import numpy as np

class TradingStrategy(Strategy):
    def __init__(self):
        self.tickers = ["AAPL", "TSLA", "META", "AMZN", "GOOGL"]
        self.lookback_period = 20  # For recent low/high
        self.entry_lookback = 10  # For entry condition check

    @property
    def assets(self):
        return self.tickers

    @property
    def interval(self):
        return "1day"

    @property
    def data(self):
        return []

    def run(self, data):
        allocation = {}
        for ticker in self.tickers:
            highs = np.array([d[ticker]["high"] for d in data["ohlcv"][-self.lookback_period:]])
            lows = np.array([d[ticker]["low"] for d in data["ohlcv"][-self.lookback_period:]])
            
            current_low = data["ohlcv"][-1][ticker]["low"]
            recent_low = min(lows)
            long_recent_low = current_low if current_low < recent_low else recent_low

            current_high = data["ohlcv"][-1][ticker]["high"]
            recent_high = max(highs[:-1])  # Exclude current day for prior high
            
            if long_recent_low < lows[-2]:  # If today's recent low is less than prior day's recent low
                long_recent_high = current_high if current_high > recent_high else highs[-2]
            else:
                long_recent_high = highs[-2]  # Prior day's high as fallback

            # Linear regression trend for the last 60 periods
            prices = np.array([d[ticker]["close"] for d in data["ohlcv"][-60:]])
            regression_slope = Momentum(ticker, {"close": prices.tolist()}, 60)[-1]
            # Determine if the linear trend is peaking
            trend_peaking = regression_slope > 0 and np.allclose(prices[-10:], prices[-1], atol=0.01)
            
            # Entry & exit logic based on linear trend and recent lows being constant
            if np.all(lows[-self.entry_lookback:] == recent_low) and trend_peaking:
                allocation[ticker] = 0.618 / len(self.tickers)  # Simplified dynamic allocation based on Fibonacci level
            else:
                allocation[ticker] = 0  # Not entering or exiting based on conditions
            
        return TargetAllocation(allocation)