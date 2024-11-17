from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import SMA, Slope
from surmount.logging import log

class TradingStrategy(Strategy):
    
    @property
    def assets(self):
        return ["AAPL"]
    
    @property
    def interval(self):
        return "1day"
    
    def run(self, data):
        # Extract close prices for easier processing
        close_prices = [data["ohlcv"][i]["AAPL"]["close"] for i in range(len(data["ohlcv"]))]

        # Calculate moving averages
        ma20 = SMA("AAPL", data["ohlcv"], 20)
        ma60 = SMA("AAPL", data["ohlcv"], 60)
        ma240 = SMA("AAPL", data["ohlcv"], 240)
        
        # Calculate slopes
        slope_ma20 = Slope("AAPL", data["ohlcv"], 20)
        slope_ma60 = Slope("AAPL", data["ohlcv"], 60)
        
        # Calculate MA differences
        ma20_ma60_difference = [ma20_val - ma60_val for ma20_val, ma60_val in zip(ma20, ma60)]
        
        # Initialize indicators
        indicator_1 = indicator_2 = False
        state = ""
        
        # Check conditions for indicators based on provided logic
        if len(ma20_ma60_difference) > 1:
            indicator_1 = ma20_ma60_difference[-2] > 0 and ma20_ma60_difference[-1] < 0
            indicator_2 = ma20_ma60_difference[-2] < 0 and ma20_ma60_difference[-1] > 0

        if indicator_1 and not indicator_2:
            state = "Start bearish"
        elif not indicator_1 and indicator_2:
            state = "Start bullish"

        # Entry or exit logic based on slope and MA differences
        allocation = 0.0

        if slope_ma20[-1] == max(slope_ma20) and slope_ma60[-1] == max(slope_ma60) and ma20_ma60_difference[-1] == max(ma20_ma60_difference):
            # Enter Condition
            log("Enter signal triggered.")
            allocation = 1.0
        elif slope_ma20[-1] != max(slope_ma20) and slope_ma60[-1] != max(slope_ma60) and ma20_ma60_difference[-1] == max(ma20_ma60_difference):
            # Exit Condition
            log("Exit signal triggered.")
            allocation = 0.0

        # Print current state
        log(state)

        return TargetAllocation({"AAPL": allocation})