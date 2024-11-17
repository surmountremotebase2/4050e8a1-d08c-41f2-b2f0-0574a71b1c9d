from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import SMA
from surmount.data import ohlcv
import numpy as np

class TradingStrategy(Strategy):
    def __init__(self):
        self.tickers = ["AAPL", "TSLA", "WMT"]

    @property
    def assets(self):
        return self.tickers

    @property
    def interval(self):
        # Using daily interval for calculation of MAs and their slopes
        return "1day"

    def calculate_slope(self, ma_values):
        # Slope calculation based on linear regression for the MA values
        # np.arange creates an array of incrementing numbers from 0 up, matching the length of ma_values
        return np.polyfit(np.arange(len(ma_values)), np.array(ma_values), 1)[0]

    def run(self, data):
        allocation = {}
        for ticker in self.tickers:
            # Calculate moving averages
            ma20 = SMA(ticker, data, 20)
            ma60 = SMA(ticker, data, 60)
            ma240 = SMA(ticker, data, 240)

            # Calculate slope of moving averages
            slope_ma20 = self.calculate_slope(ma20[-20:])
            slope_ma60 = self.calculate_slope(ma60[-60:])

            # Calculate the difference between MA20 and MA60 for current and previous day
            ma20_ma60_today = ma20[-1] - ma60[-1]
            ma20_ma60_yesterday = ma20[-2] - ma60[-2]

            # Indicators based on the Moving Average differences
            indicator_1 = ma20_ma60_yesterday > 0 and ma20_ma60_today < 0
            indicator_2 = ma20_ma60_yesterday < 0 and ma20_ma60_today > 0

            # Determine the trade signal
            signal = ""
            if indicator_1 and not indicator_2:
                signal = "Start bearish"
            elif not indicator_1 and indicator_2:
                signal = "Start bullish"

            # Check conditions for entering or exiting a position
            enter_condition = (slope_ma20 == max(ma20[-20:]) and 
                               slope_ma60 == max(ma60[-60:]) and 
                               ma20_ma60_today == max(np.diff(ma20[-20:]) - np.diff(ma60[-60:])))
            
            exit_condition = (slope_ma20 != max(ma20[-20:]) and 
                              slope_ma60 != max(ma60[-60:]) and 
                              ma20_ma60_today == max(np.diff(ma20[-20:]) - np.diff(ma60[-60:])))

            # Assign allocation based on the signal and condition
            if signal == "Start bullish" and enter_condition:
                allocation[ticker] = 1 / len(self.tickers)  # Equal portion if conditions met for bullish signal
            elif signal == "Start bearish" or exit_condition:
                allocation[ticker] = 0  # Exit the position or don't take if bearish
            else:
                allocation[ticker] = 0  # Default to no position if conditions are not clear

        return TargetAllocation(allocation)