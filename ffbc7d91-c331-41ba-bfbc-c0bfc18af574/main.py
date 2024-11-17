from surmount.base_class import Strategy, TargetAllocation
from surmount.data import Asset, MarketCap
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        self.watchlist = {}
        self.tickers = []  # Populate with suitable tickers if known in advance or dynamically add based on criteria
        self.data_list = [MarketCap(ticker) for ticker in self.tickers]  # To check market cap of each asset
        
    @property
    def assets(self):
        return self.tickers

    @property
    def interval(self):
        # The strategy description does not specify a preferred candle interval, assuming '1day' for broad coverage.
        return "1day"

    @property
    def data(self):
        return self.data_list

    def run(self, data):
        allocation_dict = {}
        for ticker in self.tickers:
            market_cap = data[("market_cap", ticker)]
            
            # Verify if the current ticker has valid market cap data and meets criteria
            if market_cap and market_cap[-1]["value"] > 10000:
                ohlcv_data = data["ohlcv"]
                close_prices = [ohlcv_data[ticker]["close"] for ticker in ohlcv_data if ticker in self.tickers]
                
                # Check if close prices are within the target range of $3 to $10
                if all(3 <= price <= 10 for price in close_prices):
                    # Calculate average close price
                    avg_close_price = sum(close_prices) / len(close_prices)

                    # Determine if the stock meets the volatility criteria
                    volatility_counter = self._calculate_volatility_swings(close_prices, avg_close_price)

                    # If stock is volatile enough, add to watchlist or update trading logic
                    if volatility_counter >= 6:
                        self._update_watchlist_and_trade_logic(ticker, avg_close_price, allocation_dict, data)

        return TargetAllocation(allocation_dict)

    def _calculate_volatility_swings(self, prices, avg_price):
        """
        Counts how many times prices have swung by >= 1% of the average price in both directions.
        """
        count = 0
        for price in prices:
            if abs((price - avg_price) / avg_price) >= 0.01:
                count += 1
        return count

    def _update_watchlist_and_trade_logic(self, ticker, avg_price, allocation_dict, data):
        """
        Implement the specific logic as described for when a stock is added to the watchlist:
        Including the buy order logic (2% below avg_price or current close, whichever is lower),
        updating limit prices, handling partial fills, and sell order placement according to strategy specified.
        
        Note: This logic is more nuanced and requires detailed implementation depending on
        how orders are managed within the Surmount trading environment (which is beyond the
        scope of this code snippet based on the provided specifications).
        """
        # Example skeleton for updating allocation dict; specific order execution logic will depend on the Surmount environment.
        current_price = data["ohlcv"][-1][ticker]["close"]
        buy_price = min(avg_price * 0.98, current_price)  # 2% below average or current, whichever is lower

        # Placeholder logic for updating allocation, real trading logic to be implemented as per Surmount's execution methods
        allocation_dict[ticker] = self._calculate_allocation_based_on_price(buy_price)

    def _calculate_allocation_based_on_price(self, price):
        """
        Placeholder for allocation calculation method. Real implementation needed based on Surmount's execution capability.
        """
        # Implement allocation calculation based on trading strategy criteria described.
        return 0.1 # This is just a placeholder.

# Note: This script outlines the high-level approach and requires filling in with the actual trading and data management logic.
# Some aspects like determining tickers based on market cap, actual price movements, trade execution,
# handling partial fills, and dynamically managing buy/sell orders need to be adjusted according to the
# platform's capabilities and available methods.