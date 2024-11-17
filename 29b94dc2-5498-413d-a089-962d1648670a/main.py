from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import SMA
from surmount.logging import log

class TradingStrategy(Strategy):
    @property
    def assets(self):
        # Define the assets in which we are interested
        return ["SPY"]

    @property
    def interval(self):
        # Set the interval for our data
        return "1day"

    def run(self, data):
        # Initialize the stake to 0
        spy_stake = 0
        
        # Calculate moving averages
        ma20 = SMA("SPY", data["ohlcv"], 20)
        ma60 = SMA("SPY", data["ohlcv"], 60)
        ma240 = SMA("SPY", data["ohlcv"], 240)
        
        if len(ma20) > 1 and len(ma60) > 1:
            # Calculate the slope for MA20 and MA60
            slope_ma20 = ma20[-1] - ma20[-2]
            slope_ma60 = ma60[-1] - ma60[-2]
             
            # Log calculated slopes
            log(f"Slope MA20: {slope_ma20}, Slope MA60: {slope_ma60}")
            
            # Determine the trading signal
            if ma20[-1] > ma60[-1]:  # Bullish signal
                spy_stake = 1
            elif ma20[-1] < ma60[-1]:  # Bearish signal
                spy_stake = 0
        
        # Return the target allocation
        return TargetAllocation({"SPY": spy_stake})