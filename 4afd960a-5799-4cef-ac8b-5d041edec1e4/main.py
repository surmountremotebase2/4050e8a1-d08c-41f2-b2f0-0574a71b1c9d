from surmount.base_class import Strategy, TargetAllocation
from surmount.data import OHLCV
from surmount.technical_indicators import SMA, Slope
from surmount.logging import log
import pandas as pd

class TradingStrategy(Strategy):
    def __init__(self):
        self.ticker = "TSLA"
        self.lookback_period = 20
        self.assessment_period = 60
    
    @property
    def interval(self):
        return "1day"  # Adjust based on the granularity you're targeting
    
    @property
    def assets(self):
        return [self.ticker]
    
    @property
    def data(self):
        # OHLCV data will automatically be included
        return []
    
    def run(self, data):
        # Extract ohlcv for easier handling
        df = pd.DataFrame(data["ohlcv"])
        # Ensure the DataFrame is sorted by date, ascending
        df.sort_values(by=[('date', self.ticker)], inplace=True)
        
        # Calculate Long Recent Low
        df['min_20d_low'] = df[('low', self.ticker)].rolling(window=self.lookback_period, min_periods=1).min()
        df['long_recent_low'] = df.apply(lambda row: row[('low', self.ticker)] if row[('low', self.ticker)] < row['min_20d_low'] else row['min_20d_low'], axis=1)
        
        # Calculate Long Recent High
        df['prior_long_recent_low'] = df['long_recent_low'].shift(1)
        df['max_20d_high'] = df[('high', self.ticker)].rolling(window=self.lookback_period, min_periods=1).max()
        df['prior_high'] = df[('high', self.ticker)].shift(1)
        df['long_recent_high'] = df.apply(
            lambda row: row['prior_high'] if (row['long_recent_low'] < row['prior_long_recent_low']) and (row[('high', self.ticker)] > row['max_20d_high']) else row['prior_high'], 
            axis=1
        )
        
        # Linear indicator over 60 days, could represent the slope of a 60 day SMA
        df['linear_60'] = Slope(self.ticker, df.to_dict(orient='records'), length=self.assessment_period)
        
        # Entry condition
        min_long_recent_low_10d = df['long_recent_low'].tail(10).min()
        is_constant = all(df['long_recent_low'].tail(10) == min_long_recent_low_10d)
        # Exit condition assumes peak in 'linear_60' - might require custom logic to determine peak
        # This example is based on a simplification and needs proper peak detection logic
        linear_60_declining = df['linear_60'].iloc[-1] < df['linear_60'].iloc[-2]
        
        # Deciding allocation
        if is_constant:
            entry_signal = 1  # Enter position
        elif linear_60_declining:
            entry_signal = 0  # Exit position, if peak is detected
        else:
            entry_signal = 0  # Hold off on any action if conditions are not met
        
        allocation_dict = {self.ticker: entry_signal}
        
        return TargetAllocation(allocation_dict)