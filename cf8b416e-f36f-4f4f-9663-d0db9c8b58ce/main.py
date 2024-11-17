from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import Slope
from surmount.logging import log
from surmount.data import Asset

class TradingStrategy(Strategy):
    
    def __init__(self):
        # Tickers to be tracked
        self.tickers = ["AAPL"]
        # No additional data required from surmount.data
        self.data_list = []

    @property
    def interval(self):
        return "1day"
    
    @property
    def assets(self):
        return self.tickers
    
    @property
    def data(self):
        return self.data_list
    
    def run(self, data):
        ohlcv = data["ohlcv"]
        aapl_data = ohlcv["AAPL"] if "AAPL" in ohlcv else []
        
        # Ensure we have at least 21 days of data for processing
        if len(aapl_data) < 21:
            return TargetAllocation({})
        
        # Calculate Long Recent Low
        recent_lows = [day["low"] for day in aapl_data[-21:]]  # Last 20 days + current day
        min_recent_low = min(recent_lows[:-1])  # Exclude current day for 20 days look-back
        long_recent_low = recent_lows[-1] if recent_lows[-1] < min_recent_low else min_recent_low
        
        # Calculate Long Recent High with conditions provided
        if long_recent_low < recent_lows[-2]:  # comparing with prior day long recent low
            recent_highs = [day["high"] for day in aapl_data[-21:]]
            max_recent_high = max(recent_highs[:-1])
            long_recent_high = recent_highs[-2] if recent_highs[-1] > max_recent_high else recent_highs[-2]  # assuming "prior date high" to be [-2]
        else:
            long_recent_high = recent_highs[-2]  # Placeholder for actual logic, as "prior date Long recent high" needs clarification
        
        # Entry Condition - Check if minimum long recent low are the same for the last 10 days
        all_same_recent_lows = all(low == long_recent_low for low in recent_lows[-11:-1])  # Excludes current day
        
        # Exit Logic Placeholder - Check for peak in linear regression (Slope over 60 periods)
        # Note: Proper peak detection might require more nuanced analysis
        linear_slope = Slope("AAPL", aapl_data, 60)
        is_peaking = linear_slope[-1] <= 0 and linear_slope[-2] > 0  # Simplified peak check
        
        allocation = {}
        if all_same_recent_lows:
            # Enter position logic - Set allocation to a value (e.g., max allocation)
            allocation["AAPL"] = 1.0
        elif is_peaking:
            # Exit position - reset allocation to 0
            allocation["AAPL"] = 0
        
        # For simplicity, this strategy only enters or exits based on given conditions and does not manage ongoing positions
        return TargetAllocation(allocation)