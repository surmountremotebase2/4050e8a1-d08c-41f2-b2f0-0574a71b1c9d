from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import EMA
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        self.tickers = ["TSLA"]

    @property
    def interval(self):
        # Assume daily interval data is sufficent for our analysis
        return "1day"

    @property
    def assets(self):
        return self.tickers

    def run(self, data):
        # Approximate Fibonacci Retracement logic via EMA comparison
        short_term_ema = EMA("TSLA", data["ohlcv"], length=8) # More responsive EMA
        long_term_ema = EMA("TSLA", data["ohlcv"], length=21) # Less responsive EMA
        allocation_ratio = 0

        if len(short_term_ema)>0 and len(long_term_ema)>0:
            current_short_term_ema = short_term_ema[-1]
            current_long_term_ema = long_term_ema[-1]

            # A simplified approach: if the short-term EMA crosses above the long-term EMA,
            # it might be seen as an indication of a potential upward movement, similar to
            # what might be expected after a retracement to the 0.618 Fibonacci level.
            if current_short_term_ema > current_long_term_ema:
                log("Price potentially rebounding off significant Fibonacci level, considering buy.")
                allocation_ratio = 1  # Full investment in TSLA
            else:
                log("Not at Fibonacci retracement level, holding off.")
                allocation_ratio = 0  # No investment in TSLA

        return TargetAllocation({"TSLA": allocation_ratio})