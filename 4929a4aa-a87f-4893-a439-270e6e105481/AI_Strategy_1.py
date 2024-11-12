from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import SMA
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        # Replace 'XYZ' with the actual ticker symbol of the asset you want to trade.
        self.ticker = "XYZ"

    @property
    def interval(self):
        # The frequency at which the strategy is evaluated. Adjust as needed.
        return "1day"

    @property
    def assets(self):
        # This strategy is designed for a single asset.
        return [self.ticker]

    @property
    def data(self):
        # No additional data sources required for this example.
        return []

    def run(self, data):
        # Running Moving Average calculations for different periods.
        ma20 = SMA(self.ticker, data["ohlcv"], 20)
        ma60 = SMA(self.ticker, data["ohlcv"], 60)
        ma240 = SMA(self.ticker, data["ohlcv"], 240)

        # Initiate a TargetAllocation object with a default allocation of 0 (no position).
        allocation = {self.ticker: 0}

        # Ensure we have enough data for all MAs by checking the length of one of them.
        # This is a simplistic check and assumes all MAs will have the same availability.
        if len(ma20) > 0 and len(ma60) > 0 and len(ma240) > 0:
            # Compare the last values of the MAs to determine if conditions for a buy are met.
            # Ensure all MAs values are available at this point to prevent index errors.
            if ma20[-1] > ma60[-1] and ma20[-1] > ma240[-1] and ma60[-1] > ma240[-1]:
                # If conditions are met, set the target allocation to 1 (100% of capital allocated to this asset).
                allocation[self.ticker] = 1
                log("MA bullish crossover detected. Going long on: " + self.ticker)
            else:
                log("MA conditions not met. No position for: " + self.ticker)

        # Return the target allocation.
        return TargetAllocation(allocation)