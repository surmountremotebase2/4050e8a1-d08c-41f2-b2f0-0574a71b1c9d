from surmount.base_class import Strategy, TargetAllocation
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        # Define the tickers of interest
        self.tickers = ["AAPL", "GOOGL"]

        # Here, one could add data requirements, such as FinancialStatement,
        # ohlcv data, etc., but for the sake of this example, and given the constraints,
        # we'll not add anything to the self.data_list as OHLCV data is implicitly included.

    @property
    def interval(self):
        # Set the data interval for analysis, assuming daily resolution suffices for this strategy
        return "1day"

    @property
    def assets(self):
        # Define the assets this strategy will trade
        return self.tickers

    def run(self, data):
        # Placeholder for allocation logic, equally divided by default
        allocation_dict = {ticker: 0.5 for ticker in self.tickers}  # Starting with a naive 50-50 split

        # Arbitrage logic based on the closing prices of AAPL and GOOGL
        try:
            aapl_close = data["ohlcv"][-1]["AAPL"]["close"]
            googl_close = data["ohlcv"][-1]["GOOGL"]["close"]

            # Example arbitrage condition: AAPL closes more than 1% higher than GOOGL
            # This simplistic logic assumes that such discrepancies will revert.
            # An actual strategy would need a far more sophisticated approach.
            if aapl_close > 1.01 * googl_close:
                # Suppose we decide to sell AAPL (expecting it to fall) and buy GOOGL (expecting it to rise).
                # The allocations weight towards GOOGL.
                allocation_dict = {"AAPL": 0.4, "GOOGL": 0.6}
            elif googl_close > 1.01 * aapl_close:
                # In the reverse situation, adjust allocations the other way.
                allocation_dict = {"AAPL": 0.6, "GOOGL": 0.4}

        except IndexError as e:
            # Handle cases where data may be insufficient to make a decision
            log(f"Insufficient data to make a decision: {e}")

        return TargetAllocation(allocation_dict)