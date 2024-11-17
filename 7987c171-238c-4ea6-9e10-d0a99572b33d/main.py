from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import SMA
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        # Define only AAPL for trading
        self.ticker = "AAPL"
        self.lookback_periods = 60  # Window for the SMA

    @property
    def assets(self):
        # List of assets this strategy will handle
        return [self.ticker]

    @property
    def interval(self):
        # Using daily interval for SMA calculation
        return "1day"

    def run(self, data):
        # Initialize allocation with no position
        allocation = {self.ticker: 0}

        # Ensure there's enough data for SMA calculation
        if len(data["ohlcv"]) >= self.lookback_periods:
            # Calculate the 60-day SMA for AAPL
            sma_60 = SMA(self.ticker, data["ohlcv"], self.lookback_periods)[-1]

            # Get the latest closing price for AAPL
            latest_close = data["ohlcv"][-1][self.ticker]["close"]

            # Logic to determine entry or exit
            if latest_close < sma_60:
                # If latest close is below the SMA, consider it "at the bottom" and enter (buy)
                log(f"Entering {self.ticker}, as price is below the 60-period SMA.")
                allocation[self.ticker] = 1  # Max allocation
            elif latest_close > sma_60:
                # If latest close is above the SMA, consider it "at the peak" and exit (sell)
                log(f"Exiting {self.ticker}, as price is above the 60-period SMA.")
                allocation[self.ticker] = 0  # No allocation

        return TargetAllocation(allocation)