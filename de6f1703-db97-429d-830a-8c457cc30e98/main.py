from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import SMA
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        self.tickers = ["AAPL"]

    @property
    def assets(self):
        return self.tickers

    @property
    def interval(self):
        return "1hour"

    def run(self, data):
        # Initialize allocation with no position
        allocation_dict = {"AAPL": 0}

        # Retrieve OHLCV data for AAPL
        aapl_data = data["ohlcv"]

        # Verify if there's enough data for the longest MA
        if len(aapl_data) >= 240:

            ma20 = SMA("AAPL", aapl_data, 20)[-1]
            ma60 = SMA("AAPL", aapl_data, 60)[-1]
            ma240 = SMA("AAPL", aapl_data, 240)[-1]

            # Conditions for entering a position
            if ma20 > ma60 and ma20 > ma240 and ma60 > ma240:
                allocation_dict["AAPL"] = 1  # Enter: Allocate 100%
            # Conditions for exiting a position
            elif ma20 < ma60 and ma20 > ma240 and ma60 > ma240:
                allocation_dict["AAPL"] = 0  # Exit: Allocate 0%

        # Log MA values for reference
        log(f"MA20: {ma20}, MA60: {ma60}, MA240: {ma240}")

        return TargetAllocation(allocation_dict)