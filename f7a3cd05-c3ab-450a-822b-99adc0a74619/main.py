from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import SMA, Slope
from surmount.logging import log

class TradingStrategy(Strategy):
    @property
    def assets(self):
        # Define the assets to be used in the strategy
        return ["AAPL"]

    @property
    def interval(self):
        # Define the interval for the data; adjust based on strategy requirements
        return "1day"

    def run(self, data):
        # Initialize stake for both long (AAPL) and short positions (not directly, but conceptually)
        long_stake = 0
        short_stake = 0

        # Calculate Moving Averages: MA20, MA60, MA240
        ma20 = SMA("AAPL", data["ohlcv"], 20)
        ma60 = SMA("AAPL", data["ohlcv"], 60)
        ma240 = SMA("AAPL", data["ohlcv"], 240)

        # Calculate Slopes: Slope of MA20, Slope of MA60
        slope_ma20 = Slope("AAPL", data["ohlcv"], 20)
        slope_ma60 = Slope("AAPL", data["ohlcv"], 60)

        if len(slope_ma20) > 0 and len(slope_ma60) > 0:
            # If slope of MA20 > slope of MA60, then long enter, short exit
            if slope_ma20[-1] > slope_ma60[-1]:
                log("Long Enter condition met. Going Long.")
                long_stake = 1  # Enter or maintain long position
                short_stake = 0  # Ensure short position is exited

            # If slope of MA20 < slope of MA60, then long exit, short enter
            elif slope_ma20[-1] < slope_ma60[-1]:
                log("Short Enter condition met. Exiting Long, if any.")
                # Conceptually shorting, but here just exiting long positions or staying out
                long_stake = 0  # Exit or avoid long position
                short_stake = 0  # Not possible to short directly; represented by having no stake

        # Return the Target Allocation. Since the platform doesn't support direct short selling,
        # 'short_stake' isn't used to define a negative position but rather to indicate absence of position.
        return TargetAllocation({"AAPL": long_stake})