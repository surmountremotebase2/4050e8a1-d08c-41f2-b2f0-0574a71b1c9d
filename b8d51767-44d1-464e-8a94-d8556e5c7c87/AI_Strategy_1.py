from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import SMA, STDEV, Slope
from surmount.data import OHLCV
import numpy as np
import pandas as pd

class TradingStrategy(Strategy):
    def __init__(self):
        # Define the ticker of interest
        self.ticker = "AAPL"

    @property
    def interval(self):
        # This defines the trading frequency. Daily data is used here.
        return "1day"

    @property
    def assets(self):
        # Specify which assets this strategy is interested in.
        return [self.ticker]

    @property
    def data(self):
        # Define what data is needed for the strategy.
        return [OHLCV(self.ticker)]

    def run(self, data):
        # Work with the stock's historical data
        historical_data = data["ohlcv"]  # Assuming this returns a list of dictionaries

        # Convert historical data to DataFrame for easier manipulation
        df = pd.DataFrame.from_records([d[self.ticker] for d in historical_data])

        # Ensure data is sorted by date, just in case
        df.sort_values(by="date", inplace=True)

        # Calculate Minimum Low and Maximum High over the past 20 days
        df["Min_Low_20D"] = df["low"].rolling(window=20).min().shift(1)
        df["Max_High_20D"] = df["high"].rolling(window=20).max().shift(1)

        # Determine Today's Long Recent Low
        df["Long_Recent_Low"] = np.where(df["low"] < df["Min_Low_20D"], df["low"], df["Min_Low_20D"])

        # Determine Today's Long Recent High
        conditions = [
            (df["Long_Recent_Low"] < df["Long_Recent_Low"].shift(1)) & (df["high"] > df["Max_High_20D"]),
            (df["Long_Recent_Low"] < df["Long_Recent_Low"].shift(1))
        ]
        choices = [df["high"].shift(1), df["Max_High_20D"].shift(1)]
        df["Long_Recent_High"] = np.select(conditions, choices, default=df["Max_High_20D"])

        # Calculate Linear Regression slope over the last 60 days to determine trend
        df["Linear_60"] = Slope(self.ticker, df.tail(60).to_dict(orient='records'), 60)

        # Entry condition - if the minimum of Long Recent Low is the same over the past 10 days
        should_enter = df["Long_Recent_Low"].tail(10).nunique() == 1

        # Exit condition - checking if Linear_60 is at its peak requires looking at a derivative or the change; using a simple diff here for illustration
        recent_trend = df["Linear_60"].diff().tail(2).tolist()
        should_exit = recent_trend[-2] > 0 and recent_trend[-1] <= 0  # Assuming a peak is where the trend recently decreased

        # Determine allocation
        allocation = 0  # Default to no position
        if should_enter:
            allocation = 1  # Enter position
        elif should_exit:
            allocation = 0  # Exit position

        # Return the target allocation
        return TargetAllocation({self.ticker: allocation})